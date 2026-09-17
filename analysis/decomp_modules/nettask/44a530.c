
void __thiscall FUN__text__0044a530(int param_1,short param_2,short param_3)

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
  *(undefined2 *)(param_1 + 0x1ae) = 0x48;
  local_8 = param_1;
  FUN__text__00408f10((int)param_2,(int)param_3,0xffffffff);
  local_8 = 0x44a580;
  FUN__text__0056ce80();
  return;
}

