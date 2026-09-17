
PVOID FUN__text1__00836de9(HANDLE param_1,LPCVOID param_2)

{
  _MEMORY_BASIC_INFORMATION local_20;
  
  VirtualQueryEx(param_1,param_2,&local_20,0x1c);
  return local_20.AllocationBase;
}

