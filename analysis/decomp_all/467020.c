
void __thiscall FUN__text__00467020(int param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  char local_20;
  uint local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = (int)*(short *)(&DAT_0061053c + param_3 * 8);
  local_20 = (&DAT_0061053e)[param_3 * 8];
  local_8 = param_1;
  if (local_20 == '\0') {
LAB__text__0046706f:
    local_18 = 0;
  }
  else if (local_20 == '\x01') {
    local_18 = (int)(char)(&DAT_0061053f)[param_3 * 8];
  }
  else if (local_20 == '\x02') {
    iVar1 = FUN__text__00468d80(param_2);
    if (((iVar1 != 0) && (iVar1 = FUN__text__0046a430(param_2), iVar1 == 0)) &&
       (local_c = FUN__text__00466e20(local_14), local_c != 0)) goto LAB__text__0046714a;
    local_1c = (uint)*(ushort *)(*(int *)(param_2 + 600) + 2);
    if (((0x22 < local_1c) || (0x27 < param_3)) ||
       (local_1c = (uint)(char)(&DAT_00618090)[local_1c + param_3 * 0x28], local_1c == 0))
    goto LAB__text__0046706f;
    local_18 = local_1c + 1;
    FUN__text__0042b2d0("char:%03d, job:%03d : palette:%03d\n",
                        *(undefined2 *)(*(int *)(param_2 + 600) + 2),param_3,local_1c);
  }
  local_c = FUN__text__00466e90(local_14,local_18);
LAB__text__0046714a:
  *(undefined4 *)(param_2 + 0x44) = *(undefined4 *)(local_c + 4);
  FUN__text__00409ef0(param_2 + 0x48);
  *(int *)(param_2 + 0x74) = local_8 + 0x2f164;
  FUN__text__0046bd30(param_2);
  for (local_10 = 0; local_10 != 5; local_10 = local_10 + 1) {
    FUN__text__00409ef0(param_2 + 0xa0 + local_10 * 0x58);
  }
  *(int *)(param_2 + 0xcc) = local_8 + 0x2f164;
  local_8 = 0x4671de;
  FUN__text__0056ce80();
  return;
}

