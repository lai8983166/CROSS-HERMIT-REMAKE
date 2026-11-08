import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from devtools import isolated_windows_vm as vm


class DedicatedVmTests(unittest.TestCase):
    def config(self):
        fields={'numvcpus':'2','memsize':'4096','cpuid.coresPerSocket':'2',
            'isolation.tools.copy.disable':'TRUE','isolation.tools.paste.disable':'TRUE',
            'isolation.tools.dnd.disable':'TRUE','sharedFolder.maxNum':'0','usb.present':'FALSE',
            'workingDir':str(vm.WORKER),'snapshotDirectory':str(vm.WORKER),
            'scsi0:0.present':'TRUE','scsi0:0.fileName':'worker.vmdk',
            'ide1:0.present':'TRUE','ide1:0.deviceType':'cdrom-image','ide1:0.fileName':str(vm.MEDIA),
            'ide1:1.present':'TRUE','ide1:1.deviceType':'cdrom-image','ide1:1.fileName':str(vm.WORKER/'windows-tools.iso'),
            'floppy0.present':'TRUE','floppy0.fileType':'file','floppy0.fileName':str(vm.WORKER/'autoinst.flp')}
        return '\n'.join(f'{k} = "{v}"'for k,v in fields.items())
    def test_only_owned_attachments_accepted(self):
        vm.validate_vmx(self.config())
        for key,value in [('scsi0:1.present','TRUE'),('sata0:0.fileName','other.vmdk'),
                ('serial0.fileName','C:/user.txt'),('sharedFolder0.present','TRUE'),('pciPassthru0.present','TRUE')]:
            with self.assertRaises(ValueError):vm.validate_vmx(self.config()+f'\n{key} = "{value}"')
    def test_host_media_wrong_resources_and_duplicates_refused(self):
        text=self.config()
        for altered in (text.replace('numvcpus = "2"','numvcpus = "8"'),
                        text.replace(str(vm.MEDIA),'C:/media.iso'),text+'\nmemsize = "4096"',
                        text.replace('scsi0:0.present = "TRUE"','scsi0:0.present = "FALSE"')):
            with self.assertRaises(ValueError):vm.validate_vmx(altered)
    def test_disk_descriptor_must_be_independent_exact_owned_extent(self):
        temp=vm.WORKER/'tmp';temp.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp)as directory,patch.object(vm,'WORKER',Path(directory)):
            path=Path(directory)/'worker.vmdk';header=bytearray(512);header[:4]=b'KDMV';struct.pack_into('<QQ',header,28,1,1)
            def put(descriptor):path.write_bytes(header+descriptor.encode().ljust(512,b'\0'))
            good='createType="monolithicSparse"\nparentCID=ffffffff\nRW 83886080 SPARSE "worker.vmdk"\n'
            put(good);vm.validate_disk(path)
            for bad in (good.replace('worker.vmdk','other.vmdk'),good.replace('ffffffff','12345678'),
                        good.replace('83886080','167772160'),good+'parentFileNameHint="original.vmdk"\n'):
                put(bad)
                with self.assertRaises(ValueError):vm.validate_disk(path)
    def test_guest_timeout_never_discloses_command_credentials(self):
        import subprocess,json
        secret='private-test-password'
        with patch.object(vm,'require_owned_root'),patch.object(Path,'read_bytes',return_value=json.dumps({'password':secret}).encode()),patch.object(vm,'environment',return_value={}),patch.object(subprocess,'run',side_effect=subprocess.TimeoutExpired(['vmrun','-gp',secret],1)):
            with self.assertRaises(RuntimeError)as caught:vm.vmrun(['list'],guest=True)
            self.assertNotIn(secret,str(caught.exception));self.assertTrue(caught.exception.__suppress_context__)


if __name__=='__main__':unittest.main()
