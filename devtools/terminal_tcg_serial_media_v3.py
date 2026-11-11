"""Create private F-drive WinPE seed media; never install or repartition Windows."""
import hashlib,json,secrets,xml.etree.ElementTree as ET
from pathlib import Path
from devtools.isolated_windows_vm import WORKER,identity
STARTUP=b'@echo off\r\nif /i not "%COMPUTERNAME%"=="CHAOMOFA-WORKER" exit /b 20\r\necho startup-entered>"C:\\ChaomofaWorker\\SerialV3\\startup-entered.txt"\r\nstart "" /b "C:\\ChaomofaWorker\\SerialV3\\agent.exe"\r\necho %errorlevel%>"C:\\ChaomofaWorker\\SerialV3\\startup-launch-exit.txt"\r\nexit /b 0\r\n'
def answer():
 ns='urn:schemas-microsoft-com:unattend';wcm='http://schemas.microsoft.com/WMIConfig/2002/State';ET.register_namespace('',ns);ET.register_namespace('wcm',wcm)
 def tag(p,n,text=None,attrs=None):
  e=ET.SubElement(p,'{'+ns+'}'+n,attrs or {});e.text=text;return e
 root=ET.Element('{'+ns+'}unattend');settings=tag(root,'settings',attrs={'pass':'windowsPE'})
 common=dict(processorArchitecture='amd64',publicKeyToken='31bf3856ad364e35',language='neutral',versionScope='nonSxS')
 intl=tag(settings,'component',attrs=dict(name='Microsoft-Windows-International-Core-WinPE',**common));lang=tag(intl,'SetupUILanguage');tag(lang,'UILanguage','en-US')
 for n in ('InputLocale','SystemLocale','UILanguage','UserLocale'):tag(intl,n,'0409:00000409'if n=='InputLocale'else'en-US')
 setup=tag(settings,'component',attrs=dict(name='Microsoft-Windows-Setup',**common));run=tag(setup,'RunSynchronous');command=tag(run,'RunSynchronousCommand',attrs={'{'+wcm+'}action':'add'})
 tag(command,'Order','1');tag(command,'Path','cmd.exe /d /c A:\\SEED.CMD');tag(command,'Description','Copy owned serial control into an existing isolated Windows child, then shut down')
 tag(tag(setup,'UserData'),'AcceptEula','true')
 return ET.tostring(root,encoding='utf-8',xml_declaration=True)
def seed_cmd():
 return b'@echo off\r\nsetlocal EnableExtensions EnableDelayedExpansion\r\nif /i not "%SystemDrive%"=="X:" exit /b 20\r\nif not exist X:\\Windows\\System32\\wpeutil.exe exit /b 21\r\necho started>A:\\SEED.START\r\nset COUNT=0\r\nset TARGET=\r\nfor %%D in (C D E F G H I J K L M N O P Q R S T U V W Y Z) do (\r\n if exist %%D:\\Windows\\System32\\config\\SYSTEM if exist %%D:\\ChaomofaWorker (\r\n  set /a COUNT+=1\r\n  set TARGET=%%D:\r\n )\r\n)\r\nif not "!COUNT!"=="1" goto fail\r\nif exist "!TARGET!\\ChaomofaWorker\\SerialV3" goto fail\r\nmkdir "!TARGET!\\ChaomofaWorker\\SerialV3"\r\nif errorlevel 1 goto fail\r\ncopy /b A:\\AGENT.EXE "!TARGET!\\ChaomofaWorker\\SerialV3\\agent.exe" >A:\\COPY.LOG\r\nif errorlevel 1 goto fail\r\ncopy /b A:\\CONFIG.TXT "!TARGET!\\ChaomofaWorker\\SerialV3\\CONFIG.TXT" >>A:\\COPY.LOG\r\nif errorlevel 1 goto fail\r\nreg query HKLM\\CMF_SERIAL_SEED_V3 >nul 2>&1\r\nif not errorlevel 1 goto fail\r\nreg load HKLM\\CMF_SERIAL_SEED_V3 "!TARGET!\\Windows\\System32\\config\\SOFTWARE" >A:\\REG.LOG\r\nif errorlevel 1 goto fail\r\nset HIVE_LOADED=1\r\nset ORIGINAL=\r\nfor /f "tokens=2,*" %%A in (\'reg query "HKLM\\CMF_SERIAL_SEED_V3\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon" /v Userinit 2^>nul\') do if "%%A"=="REG_SZ" set "ORIGINAL=%%B"\r\nif not "!ORIGINAL!"=="C:\\Windows\\system32\\userinit.exe," goto fail\r\necho !ORIGINAL!>A:\\USERINIT.BEFORE\r\nreg add "HKLM\\CMF_SERIAL_SEED_V3\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon" /v Userinit /t REG_SZ /d "C:\\Windows\\system32\\userinit.exe,C:\\ChaomofaWorker\\SerialV3\\agent.exe," /f >>A:\\REG.LOG\r\nif errorlevel 1 goto fail\r\nreg query "HKLM\\CMF_SERIAL_SEED_V3\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon" /v Userinit >A:\\USERINIT.AFTER\r\nif errorlevel 1 goto fail\r\nreg unload HKLM\\CMF_SERIAL_SEED_V3 >>A:\\REG.LOG\r\nif errorlevel 1 goto fail\r\nset HIVE_LOADED=\r\necho seed-complete>A:\\SEED.OK\r\necho !TARGET!>>A:\\SEED.OK\r\nwpeutil shutdown\r\nexit /b 0\r\n:fail\r\nif "!HIVE_LOADED!"=="1" reg unload HKLM\\CMF_SERIAL_SEED_V3 >>A:\\REG.LOG\r\necho seed-failed>A:\\SEED.FAIL\r\nwpeutil shutdown\r\nexit /b 1\r\n'

def main():
 from pyfatfs.PyFat import PyFat
 from pyfatfs.PyFatFS import PyFatFS
 out=WORKER/'tcg-serial-seed-v3';out.mkdir(exist_ok=False)
 build=WORKER/'tcg-serial-agent-build-v3';manifest=json.loads((build/'manifest.json').read_bytes());exe=Path(manifest['executable']['path']);raw=exe.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=manifest['executable']['sha256']:raise ValueError('compiled agent identity')
 key=secrets.token_hex(32);(out/'control-key.private').write_text(key,encoding='ascii')
 floppy=out/'seed.private.flp';floppy.touch(exist_ok=False);fat=PyFat();fat.mkfs(str(floppy),fat_type=PyFat.FAT_TYPE_FAT12,size=1440*1024,media_type=0xF0);fat.close()
 files={'Autounattend.xml':answer(),'SEED.CMD':seed_cmd(),'AGENT.EXE':raw,'CONFIG.TXT':(key+'\r\n').encode()}
 with PyFatFS(str(floppy))as fs:
  for name,data in files.items():fs.writebytes(name,data)
 with PyFatFS(str(floppy),read_only=True)as fs:
  for name,data in files.items():
   if fs.readbytes(name)!=data:raise ValueError('FAT byte identity')
 public={name:dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())for name,data in files.items()}
 (out/'media-manifest.json').write_text(json.dumps(dict(accepted=False,floppy=identity(floppy),files=public,private_key_not_in_report=True,no_disk_format_or_install_directive=True),indent=2))
 (out/'seed-source.cmd').write_bytes(files['SEED.CMD']);(out/'answer-source.xml').write_bytes(files['Autounattend.xml'])
 print(json.dumps(dict(files=public,floppy_bytes=floppy.stat().st_size)))
if __name__=='__main__':main()
