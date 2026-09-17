
uint FUN__text1__0082c23e(uint param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 uVar2;
  uint uVar3;
  int local_3c;
  int local_34 [10];
  code *local_c;
  undefined4 local_8;
  
  local_34[0] = 0xf7;
  local_34[1] = 0x8f;
  local_34[2] = 0x33;
  local_34[3] = 0x7f;
  local_34[4] = 0x35;
  local_34[5] = 0xe7;
  local_34[6] = 0xab;
  local_34[7] = 0x49;
  local_34[8] = 9;
  iVar1 = local_34[param_1 >> 9 & 7];
  local_3c = iVar1 % 0x14;
  if (iVar1 / 0x14 == local_3c) {
    local_3c = (local_3c + 1) % 0x14;
  }
  local_c = (code *)(*(uint *)(&DAT_00874450 + iVar1 * 4) ^
                     *(uint *)(&DAT_0086e2cc + (iVar1 / 0x14) * 4) ^
                    *(uint *)(&DAT_0086e2cc + local_3c * 4));
  local_8 = (*(code *)(&PTR_DAT_00872c00)[(char)(&DAT_00872ca0)[iVar1]])(param_2,7);
  uVar2 = (*local_c)(local_8,param_3);
  uVar3 = (*(code *)(&PTR_DAT_00872c50)[(char)(&DAT_00872ca0)[iVar1]])(uVar2);
  return uVar3 & 1;
}

