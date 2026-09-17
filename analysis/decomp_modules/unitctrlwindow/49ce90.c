
void __fastcall FUN__text__0049ce90(int param_1)

{
  short sVar1;
  undefined1 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  short local_1c;
  short local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_68;
  for (iVar3 = 0x19; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_20 = param_1 + 0x109860;
  local_14 = (int)*(short *)(param_1 + 0x109d4e);
  *(undefined2 *)(param_1 + 0x109d4e) = 0xffff;
  local_8 = param_1;
  if (*(short *)(param_1 + 0x30992) == -1) {
LAB__text__0049cf66:
    if ((*(int *)(local_8 + 0x108b50) == 0) || (*(char *)(local_8 + 0x108b3a) == '\0'))
    goto LAB__text__0049d144;
    local_28 = 0;
    for (local_c = 0; local_c != *(int *)(local_8 + 0x108b50); local_c = local_c + 1) {
      local_24 = *(int *)(local_8 + 0x108b60 + local_c * 4);
      iVar3 = FUN__text__0046a430(local_24);
      if (iVar3 != 0) {
        local_28 = local_24;
        local_10 = (int)*(short *)(local_24 + 2);
        goto LAB__text__0049d065;
      }
    }
    local_28 = *(int *)(local_8 + 0x108b60);
    sVar1 = *(short *)(local_28 + 2);
  }
  else {
    iVar3 = *(int *)(param_1 + 0x80dd8 + *(short *)(param_1 + 0x30992) * 0x520);
    local_18 = (short)((int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0x1fU)) >> 5);
    iVar3 = *(int *)(param_1 + 0x80ddc + *(short *)(param_1 + 0x30992) * 0x520);
    local_1c = (short)((int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0xfU)) >> 4);
    iVar3 = FUN__text__0043c160((int)local_18,(int)local_1c);
    if (iVar3 == 0) goto LAB__text__0049cf66;
    sVar1 = *(short *)(local_8 + 0x30992);
  }
  local_10 = (int)sVar1;
  iVar3 = *(int *)(local_8 + 0x80dd8 + local_10 * 0x520);
  local_18 = (short)((int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0x1fU)) >> 5);
  iVar3 = *(int *)(local_8 + 0x80ddc + local_10 * 0x520);
  local_1c = (short)((int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0xfU)) >> 4);
  iVar3 = FUN__text__0043c160((int)local_18,(int)local_1c);
  if (iVar3 != 0) {
LAB__text__0049d065:
    if (local_14 != local_10) {
      FUN__text__0040ac90(local_20 + 0x48);
      *(undefined4 *)(local_20 + 0x44) = *(undefined4 *)(local_8 + 0x80b30 + local_10 * 0x520);
      *(undefined4 *)(local_20 + 600) = *(undefined4 *)(local_8 + 0x80d44 + local_10 * 0x520);
      FUN__text__00409ef0(local_20 + 0x48);
      FUN__text__0046c040(local_20,2);
      FUN__text__00465040(local_20 + 0x48,1,(int)*(char *)(local_20 + 0x28a));
      *(undefined2 *)(local_20 + 10) = 0;
    }
    *(undefined2 *)(local_20 + 0x4ee) = (undefined2)local_10;
    uVar2 = FUN__text__0040a100(local_20 + 0x48);
    *(undefined1 *)(local_20 + 4) = uVar2;
    *(short *)(local_20 + 10) = *(short *)(local_20 + 10) + 1;
  }
LAB__text__0049d144:
  local_8 = 0x49d151;
  FUN__text__0056ce80();
  return;
}

