// Read-only bounded native-64 loader walk for an owned WOW64 fixture.
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;
public static class OwnedWow64Module {
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr OpenProcess(uint a,bool i,uint p);
 [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr h);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool ReadProcessMemory(IntPtr h,IntPtr a,byte[] b,UIntPtr n,out UIntPtr read);
 [DllImport("kernel32.dll")] static extern bool IsWow64Process(IntPtr h,out bool wow);
 [DllImport("ntdll.dll")] static extern int NtQueryInformationProcess(IntPtr h,int c,byte[] b,int n,out int returned);
 static byte[] Read(IntPtr h,ulong address,int size){
  if(address==0||address>=0x800000000000UL||size<1||size>1024)throw new Exception("bounded user read");
  byte[] b=new byte[size];UIntPtr n;
  if(!ReadProcessMemory(h,new IntPtr((long)address),b,(UIntPtr)size,out n)||n.ToUInt64()!=(ulong)size)throw new Exception("exact user read");return b;
 }
 static string Name(IntPtr h,byte[] b,int offset){
  int n=BitConverter.ToUInt16(b,offset);if(n<2||n>512||(n&1)!=0)throw new Exception("bounded module name");
  return Encoding.Unicode.GetString(Read(h,BitConverter.ToUInt64(b,offset+8),n));
 }
 public static object Find(uint pid){
  if(IntPtr.Size!=8)throw new Exception("native64 reader required");
  IntPtr h=OpenProcess(0x410,false,pid);if(h==IntPtr.Zero)throw new Exception("owned process open");
  try{
   bool wow;if(!IsWow64Process(h,out wow)||!wow)throw new Exception("WOW64 target required");
   byte[] pbi=new byte[48];int n;if(NtQueryInformationProcess(h,0,pbi,48,out n)!=0||n!=48)throw new Exception("native PBI");
   ulong peb=BitConverter.ToUInt64(pbi,8),ldr=BitConverter.ToUInt64(Read(h,peb+0x18,8),0),head=ldr+0x10;
   ulong node=BitConverter.ToUInt64(Read(h,head,8),0);HashSet<ulong> seen=new HashSet<ulong>();
   for(int i=0;i<64&&node!=head;i++){
    if(!seen.Add(node))throw new Exception("loader cycle");byte[] b=Read(h,node,0x68);
    string name=Name(h,b,0x58);
    if(String.Equals(name,"wow64cpu.dll",StringComparison.OrdinalIgnoreCase))return new {pid=pid,peb=peb,ldr=ldr,entry=node,name=name,path=Name(h,b,0x48),image_base=BitConverter.ToUInt64(b,0x30),size=BitConverter.ToUInt32(b,0x40),nodes=i+1};
    node=BitConverter.ToUInt64(b,0);
   }
   throw new Exception("module absent within bounded loader walk");
  }finally{CloseHandle(h);}
 }
}
