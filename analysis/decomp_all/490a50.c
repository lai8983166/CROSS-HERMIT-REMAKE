
void FUN__text__00490a50(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  byte *local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (byte *)(param_2 + 0x14 + param_1 * 0x10);
  iVar1 = FUN__text__004690a0(param_2);
  if (iVar1 == 0) {
    if (*local_c == 0) goto LAB__text__00490b10;
    if ((*(int *)(local_c + 8) == 0) ||
       (*(int *)(local_c + 8) = *(int *)(local_c + 8) + -1, *(int *)(local_c + 8) != 0)) {
      if (*(int *)(&DAT_006190d0 + (uint)*local_c * 4) != 0) {
        (**(code **)(&DAT_006190d0 + (uint)*local_c * 4))(local_8,local_c,param_2);
        FUN__text__0056ce80();
      }
      goto LAB__text__00490b10;
    }
  }
  FUN__text__004902e0(param_2,local_c,param_1);
LAB__text__00490b10:
  local_8 = 0x490b1d;
  FUN__text__0056ce80();
  return;
}

