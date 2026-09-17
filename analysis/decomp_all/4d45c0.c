
void FUN__text__004d45c0(short param_1)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  uint local_14;
  uint local_10;
  short local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = -1;
  if ((param_1 != 0) && (sVar1 = FUN__text__004d46e0(param_1), sVar1 != 0)) {
    if (param_1 < 0x65) {
      local_10 = local_10 & 0xffff0000;
      while ((int)(local_10 & 0xffff) < (int)DAT_007a5260) {
        if (*(short *)(&DAT_007a5210 + (local_10 & 0xffff) * 2) == param_1) {
          local_c = (short)local_10;
          break;
        }
        local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
      }
    }
    else {
      local_14 = local_14 & 0xffff0000;
      while ((int)(local_14 & 0xffff) < (int)DAT_007a528a) {
        if (*(short *)(&DAT_007a5262 + (local_14 & 0xffff) * 2) == param_1) {
          local_c = (short)local_14;
          break;
        }
        local_14 = CONCAT22(local_14._2_2_,(short)local_14 + 1);
      }
    }
  }
  local_8 = 0x4d46d3;
  FUN__text__0056ce80();
  return;
}

