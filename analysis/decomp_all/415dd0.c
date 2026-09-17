
void __thiscall FUN__text__00415dd0(int param_1,int param_2,int param_3,undefined4 param_4)

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
  *(int *)(param_1 + 0xb310) = *(int *)(param_1 + 0xb310) + 1;
  if ((*(int *)(param_1 + 0x1090) != 0) && (*(int *)(param_1 + 0xb1a0) != 0)) {
    local_8 = param_1;
    FUN__text__00402780((float)param_2,(float)param_3,param_4,&DAT_00799a50,0);
  }
  local_8 = 0x415e4e;
  FUN__text__0056ce80();
  return;
}

