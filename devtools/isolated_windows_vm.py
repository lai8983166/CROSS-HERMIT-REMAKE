"""Prepare and control only the project's dedicated F: Windows test VM.

No host UI input. Secrets and VM/media/runtime files stay outside Git on F:.
Provisioning is not a game compatibility or reverse-engineering acceptance.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import struct
import subprocess
import time
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

ROOT=Path(__file__).resolve().parents[1]
WORKER=ROOT/'.venv-audit/native-worker'
VMWARE=Path('C:/虚拟机')
VMX=WORKER/'chaomofa-worker.vmx'
MEDIA=WORKER/'SERVER_EVAL_x64FRE_en-us.iso'
MEDIA_BYTES=5044094976


def environment():
    temp=WORKER/'tmp';temp.mkdir(parents=True,exist_ok=True)
    return dict(os.environ,TEMP=str(temp),TMP=str(temp))


def require_owned_root():
    if ROOT.drive.upper()!='F:' or WORKER.resolve()!=ROOT/'.venv-audit/native-worker':
        raise ValueError('all new worker data must remain in the owned F: directory')
    WORKER.mkdir(parents=True,exist_ok=True)


def identity(path):
    h=hashlib.sha256()
    with Path(path).open('rb')as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return dict(path=str(path),bytes=Path(path).stat().st_size,sha256=h.hexdigest())


def vmrun(args,*,guest=False,timeout=60):
    require_owned_root()
    command=[str(VMWARE/'vmrun.exe'),'-T','ws']
    if guest:
        secret=json.loads((WORKER/'credentials.private.json').read_bytes())
        command+=['-gu','Administrator','-gp',secret['password']]
    command+=list(map(str,args))
    # Never print argv: guest control credentials must not enter evidence/logs.
    try:r=subprocess.run(command,cwd=WORKER,env=environment(),capture_output=True,timeout=timeout)
    except subprocess.TimeoutExpired:raise RuntimeError('vmrun exceeded bounded timeout; command credentials withheld')from None
    except OSError:raise RuntimeError('vmrun could not be executed; command credentials withheld')from None
    output=r.stdout.decode('utf8',errors='replace').strip()
    if guest:output=output.replace(secret['password'],'[redacted]')
    if r.returncode:raise RuntimeError('vmrun failed: '+output[:1200])
    return output


def validate_vmx(text):
    fields={}
    for line in text.splitlines():
        if '=' in line:
            k,v=line.split('=',1);k=k.strip()
            if k in fields:raise ValueError('duplicate VMX property')
            fields[k]=v.strip().strip('"')
    expected={'numvcpus':'2','memsize':'4096','cpuid.coresPerSocket':'2',
        'isolation.tools.copy.disable':'TRUE','isolation.tools.paste.disable':'TRUE',
        'isolation.tools.dnd.disable':'TRUE','sharedFolder.maxNum':'0','usb.present':'FALSE'}
    if any(fields.get(k)!=v for k,v in expected.items()):raise ValueError('dedicated resource/input isolation configuration')
    if fields.get('scsi0:0.fileName')!='worker.vmdk':raise ValueError('only project-owned virtual disk')
    for key in ('workingDir','snapshotDirectory'):
        if Path(fields.get(key,'')).resolve()!=WORKER.resolve():raise ValueError('runtime files must stay on F:')
    attachments={'scsi0:0':{'present':'TRUE','fileName':'worker.vmdk'},
        'ide1:0':{'present':'TRUE','deviceType':'cdrom-image','fileName':str(MEDIA)},
        'ide1:1':{'present':'TRUE','deviceType':'cdrom-image','fileName':str(WORKER/'windows-tools.iso')},
        'floppy0':{'present':'TRUE','fileType':'file','fileName':str(WORKER/'autoinst.flp')}}
    for key,value in fields.items():
        match=re.match(r'((?:scsi|sata|ide|nvme)\d+:\d+|floppy\d+)\.(.+)',key)
        if match:
            device,property_=match.groups()
            if device not in attachments:raise ValueError('unexpected attached storage device')
            if property_ in ('deviceType','fileType','fileName','present')and value!=attachments[device].get(property_):
                raise ValueError('only declared owned storage and optical images')
            if property_=='redo'and value!='':raise ValueError('external redo disk forbidden')
        if re.match(r'(?:sharedFolder\d+|serial\d+|parallel\d+|pciPassthru\d+|usb\.autoConnect)\.',key):
            raise ValueError('host device/folder passthrough forbidden')
    for device,props in attachments.items():
        if any(fields.get(device+'.'+k)!=v for k,v in props.items()):raise ValueError('complete owned attachments required')
    return fields


def validate_disk(path):
    path=Path(path)
    if path.resolve()!=WORKER/'worker.vmdk':raise ValueError('only project disk')
    with path.open('rb')as stream:
        header=stream.read(512)
        if len(header)!=512 or header[:4]!=b'KDMV':raise ValueError('owned sparse VMDK header')
        offset,size=struct.unpack_from('<QQ',header,28)
        if not 0<offset<=128 or not 0<size<=128:raise ValueError('bounded embedded disk descriptor')
        stream.seek(offset*512);descriptor=stream.read(size*512).split(b'\0',1)[0].decode('ascii')
    if ('createType="monolithicSparse"'not in descriptor or 'parentCID=ffffffff'not in descriptor
            or 'parentFileNameHint'in descriptor):raise ValueError('new independent sparse disk only')
    extents=[line.strip()for line in descriptor.splitlines()if re.match(r'^(RW|RDONLY|NOACCESS)\s',line)]
    if extents!=['RW 83886080 SPARSE "worker.vmdk"']:raise ValueError('exact owned 40 GiB disk extent')
    return dict(maximum_bytes=40*1024**3,descriptor_sha256=hashlib.sha256(descriptor.encode()).hexdigest())


def install_image():
    import pycdlib
    iso=pycdlib.PyCdlib();iso.open(str(MEDIA))
    try:
        with iso.open_file_from_iso(udf_path='/sources/install.wim')as f:
            header=f.read(208)
            if header[:8]!=b'MSWIM\0\0\0':raise ValueError('original WIM signature')
            packed,offset,original=struct.unpack_from('<QQQ',header,72);size=packed&((1<<56)-1)
            if packed>>56 & 4 or not 0<size<=1024*1024 or original!=size:raise ValueError('bounded uncompressed WIM XML')
            f.seek(offset);raw=f.read(size)
    finally:iso.close()
    root=ET.fromstring(raw);images=[dict(index=int(i.attrib['INDEX']),name=i.findtext('NAME'),
        installation_type=i.findtext('WINDOWS/INSTALLATIONTYPE'),edition=i.findtext('WINDOWS/EDITIONID'),
        architecture=i.findtext('WINDOWS/ARCH'))for i in root.findall('IMAGE')]
    selected=[i for i in images if i['name']=='Windows Server 2022 SERVERSTANDARD'and
              i['installation_type']=='Server'and i['edition']=='ServerStandardEval'and i['architecture']=='9']
    if len(selected)!=1:raise ValueError('one original Standard evaluation Desktop Experience image required')
    return dict(images=images,selected=selected[0],xml_sha256=hashlib.sha256(raw).hexdigest())


def answer_file(password,image_name='Windows Server 2022 SERVERSTANDARD'):
    password=escape(password)
    image_name=escape(image_name)
    return f'''<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
 <settings pass="windowsPE">
  <component name="Microsoft-Windows-International-Core-WinPE" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS">
   <SetupUILanguage><UILanguage>en-US</UILanguage></SetupUILanguage><InputLocale>0409:00000409</InputLocale><SystemLocale>zh-CN</SystemLocale><UILanguage>en-US</UILanguage><UserLocale>en-US</UserLocale>
  </component>
  <component name="Microsoft-Windows-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State">
   <DiskConfiguration><Disk wcm:action="add"><DiskID>0</DiskID><WillWipeDisk>true</WillWipeDisk><CreatePartitions>
    <CreatePartition wcm:action="add"><Order>1</Order><Type>Primary</Type><Size>500</Size></CreatePartition>
    <CreatePartition wcm:action="add"><Order>2</Order><Type>Primary</Type><Extend>true</Extend></CreatePartition>
   </CreatePartitions><ModifyPartitions>
    <ModifyPartition wcm:action="add"><Order>1</Order><PartitionID>1</PartitionID><Format>NTFS</Format><Label>System</Label><Active>true</Active></ModifyPartition>
    <ModifyPartition wcm:action="add"><Order>2</Order><PartitionID>2</PartitionID><Format>NTFS</Format><Label>Windows</Label><Letter>C</Letter></ModifyPartition>
   </ModifyPartitions></Disk><WillShowUI>OnError</WillShowUI></DiskConfiguration>
   <ImageInstall><OSImage><InstallFrom><MetaData wcm:action="add"><Key>/IMAGE/NAME</Key><Value>{image_name}</Value></MetaData></InstallFrom>
    <InstallTo><DiskID>0</DiskID><PartitionID>2</PartitionID></InstallTo><WillShowUI>OnError</WillShowUI></OSImage></ImageInstall>
   <UserData><AcceptEula>true</AcceptEula><FullName>Chaomofa Test Worker</FullName><Organization>Local compatibility evaluation</Organization></UserData>
  </component>
 </settings>
 <settings pass="specialize">
  <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS"><ComputerName>CHAOMOFA-WORKER</ComputerName><TimeZone>China Standard Time</TimeZone></component>
 </settings>
 <settings pass="oobeSystem">
  <component name="Microsoft-Windows-International-Core" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS"><InputLocale>0409:00000409</InputLocale><SystemLocale>zh-CN</SystemLocale><UILanguage>en-US</UILanguage><UserLocale>en-US</UserLocale></component>
  <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State">
   <OOBE><HideEULAPage>true</HideEULAPage><HideOnlineAccountScreens>true</HideOnlineAccountScreens><HideWirelessSetupInOOBE>true</HideWirelessSetupInOOBE><ProtectYourPC>3</ProtectYourPC></OOBE>
   <UserAccounts><AdministratorPassword><Value>{password}</Value><PlainText>true</PlainText></AdministratorPassword></UserAccounts>
   <AutoLogon><Password><Value>{password}</Value><PlainText>true</PlainText></Password><Enabled>true</Enabled><Username>Administrator</Username><LogonCount>8</LogonCount></AutoLogon>
   <FirstLogonCommands><SynchronousCommand wcm:action="add"><Order>1</Order><Description>Install dedicated worker tools</Description><CommandLine>powershell.exe -NoProfile -ExecutionPolicy Bypass -File A:\BOOT.PS1</CommandLine></SynchronousCommand></FirstLogonCommands>
  </component>
 </settings>
</unattend>
'''


BOOTSTRAP=r'''$ErrorActionPreference = 'Stop'
$work = 'C:\ChaomofaWorker'
New-Item -ItemType Directory -Path $work -Force | Out-Null
Start-Transcript -Path "$work\bootstrap.log"
try {
 $installer = @('D','E','F','G','H') | ForEach-Object { "${_}:\setup64.exe" } | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
 if(-not $installer){throw 'VMware Tools optical installer not found'}
 $process=Start-Process -FilePath $installer -ArgumentList '/S /v"/qn REBOOT=ReallySuppress"' -WindowStyle Hidden -Wait -PassThru
 if($process.ExitCode -notin @(0,3010)){throw "VMware Tools exit $($process.ExitCode)"}
 Set-Service -Name AudioEndpointBuilder -StartupType Automatic
 Set-Service -Name Audiosrv -StartupType Automatic
 @{status='tools_installed';exit_code=$process.ExitCode;utc=[DateTime]::UtcNow.ToString('o')} | ConvertTo-Json | Set-Content "$work\bootstrap.json"
 Stop-Transcript
 Restart-Computer -Force
} catch {
 @{status='failed';error=$_.Exception.Message} | ConvertTo-Json | Set-Content "$work\bootstrap.json"
 Stop-Transcript
 exit 1
}
'''


def prepare():
    require_owned_root()
    if VMX.exists()or (WORKER/'worker.vmdk').exists():raise ValueError('refusing to overwrite existing worker')
    if not MEDIA.is_file()or MEDIA.stat().st_size!=MEDIA_BYTES:raise ValueError('complete official installation media required')
    source=json.loads((WORKER/'media-source.json').read_bytes());media_identity=identity(MEDIA)
    if source.get('download_complete')is not True or media_identity['sha256']!=source.get('sha256'):
        raise ValueError('complete recorded Microsoft media identity required')
    image=install_image()
    account=subprocess.run(['whoami'],capture_output=True,text=True,check=True).stdout.strip()
    acl=subprocess.run(['icacls',str(WORKER),'/inheritance:r','/grant:r',account+':(OI)(CI)F','SYSTEM:(OI)(CI)F'],capture_output=True)
    if acl.returncode:raise ValueError('private local bootstrap ACL required')
    tools_media=WORKER/'windows-tools.iso'
    if not tools_media.exists():shutil.copyfile(VMWARE/'windows.iso',tools_media)
    if identity(tools_media)['sha256']!=identity(VMWARE/'windows.iso')['sha256']:
        raise ValueError('unaltered installed VMware Tools media')
    from pyfatfs.PyFat import PyFat
    from pyfatfs.PyFatFS import PyFatFS
    credential=WORKER/'credentials.private.json'
    if credential.exists():raise ValueError('inspect existing private bootstrap before preparing')
    password='Cmf!'+secrets.token_urlsafe(24)+'a9'
    credential.write_text(json.dumps(dict(password=password)),encoding='utf8')
    # Private bootstrap files are local only, never copied into Git evidence.
    floppy=WORKER/'autoinst.flp';floppy.touch(exist_ok=False)
    fat=PyFat();fat.mkfs(str(floppy),fat_type=PyFat.FAT_TYPE_FAT12,size=1440*1024,media_type=0xF0);fat.close()
    with PyFatFS(str(floppy))as fs:
        fs.writebytes('Autounattend.xml',answer_file(password,image['selected']['name']).encode('utf8'))
        fs.writebytes('BOOT.PS1',BOOTSTRAP.encode('utf8'))
    fields={'.encoding':'UTF-8','config.version':'8','virtualHW.version':'18',
        'displayName':'Chaomofa isolated Windows worker','guestOS':'windows2019srv-64',
        'firmware':'bios','bios.bootOrder':'hdd,cdrom','numvcpus':'2','cpuid.coresPerSocket':'2','memsize':'4096',
        'scsi0.present':'TRUE','scsi0.virtualDev':'lsisas1068','scsi0:0.present':'TRUE','scsi0:0.fileName':'worker.vmdk',
        'ide1:0.present':'TRUE','ide1:0.deviceType':'cdrom-image','ide1:0.fileName':str(MEDIA),
        'ide1:1.present':'TRUE','ide1:1.deviceType':'cdrom-image','ide1:1.fileName':str(tools_media),
        'floppy0.present':'TRUE','floppy0.fileType':'file','floppy0.fileName':str(floppy),
        'floppy0.startConnected':'TRUE','ethernet0.present':'TRUE','ethernet0.connectionType':'nat',
        'ethernet0.virtualDev':'e1000e','ethernet0.startConnected':'TRUE',
        'usb.present':'FALSE','sound.present':'TRUE','sound.virtualDev':'hdaudio','sound.fileName':'-1',
        'mks.enable3d':'TRUE','svga.vramSize':'134217728','svga.autodetect':'FALSE',
        'svga.maxWidth':'1280','svga.maxHeight':'960','tools.syncTime':'FALSE',
        'isolation.tools.copy.disable':'TRUE','isolation.tools.paste.disable':'TRUE','isolation.tools.dnd.disable':'TRUE',
        'sharedFolder.maxNum':'0','workingDir':str(WORKER),'snapshotDirectory':str(WORKER),
        'mainMem.useNamedFile':'TRUE','priority.ungrabbed':'idle','uuid.action':'create','msg.autoAnswer':'TRUE'}
    fields['pciBridge0.present']='TRUE'
    for bridge in range(4,8):
        fields.update({f'pciBridge{bridge}.present':'TRUE',f'pciBridge{bridge}.virtualDev':'pcieRootPort',f'pciBridge{bridge}.functions':'8'})
    text=''.join(f'{k} = "{v}"\n'for k,v in fields.items());validate_vmx(text)
    disk=subprocess.run([str(VMWARE/'vmware-vdiskmanager.exe'),'-c','-s','40GB','-a','lsilogic','-t','0',str(WORKER/'worker.vmdk')],
        env=environment(),cwd=WORKER,capture_output=True,timeout=120)
    if disk.returncode:raise RuntimeError('dedicated disk creation failed')
    disk_identity=validate_disk(WORKER/'worker.vmdk')
    VMX.write_text(text,encoding='utf8')
    manifest=dict(schema_version=1,created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
        vmx=identity(VMX),media=media_identity,tools_media=identity(tools_media),install_image=image,disk=disk_identity,
        resources=dict(vcpus=2,memory_mib=4096,disk_max_gib=40),
        evaluation_days=180,guest_graphics_compatible=False,input_isolation_verified=False,
        reverse_acceptance=False,private_bootstrap_not_for_git=True)
    (WORKER/'provision.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
    return manifest


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','start','status','stop'])
    a=p.parse_args();require_owned_root()
    if a.action=='prepare':result=prepare()
    elif a.action=='start':
        validate_vmx(VMX.read_text(encoding='utf8'));validate_disk(WORKER/'worker.vmdk');result=vmrun(['start',VMX,'nogui'],timeout=60)
    elif a.action=='status':result=vmrun(['list'])
    else:result=vmrun(['stop',VMX,'soft'])
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
