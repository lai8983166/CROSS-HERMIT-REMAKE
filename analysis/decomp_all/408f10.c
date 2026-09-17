
void __thiscall
FUN__text__00408f10(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(char *)(param_1 + 0x66) = (char)((uint)param_4 >> 0x10);
  *(char *)(param_1 + 0x65) = (char)((uint)param_4 >> 8);
  *(char *)(param_1 + 100) = (char)param_4;
  local_8 = param_1;
  FUN__text__00408f90(param_2,param_3);
  local_8 = 0x408f7c;
  FUN__text__0056ce80();
  return;
}

