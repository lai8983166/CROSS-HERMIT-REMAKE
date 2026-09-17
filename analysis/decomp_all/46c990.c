
void FUN__text__0046c990(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined *local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = &DAT_006c2dc8 + param_2 * 0x48;
  FUN__text__00472550(param_1,1,-(int)*(short *)(&DAT_006c2dd0 + param_2 * 0x48));
  local_8 = 0x46c9e1;
  FUN__text__0056ce80();
  return;
}

