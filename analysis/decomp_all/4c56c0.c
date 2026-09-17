
void FUN__text__004c56c0(undefined4 param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  undefined1 local_18;
  int local_14;
  uint local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_2;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(param_2 + 4) >> 0x1c,
                              *(uint *)(param_2 + 4) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9250) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 8) >> 0x1c,
                              *(uint *)(local_c + 8) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9254) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 0xc) >> 0x1c,
                              *(uint *)(local_c + 0xc) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9258) = uVar1;
  local_10 = CONCAT31(local_10._1_3_,*(byte *)(local_8 + 0x9250));
  local_14 = local_8 + 0x1ce + (uint)*(byte *)(local_8 + 0x9250) * 0x12;
  local_18 = FUN__text__004c7070();
  FUN__text__004c6d70();
  FUN__text__004c6dd0(local_10 & 0xff);
  FUN__text__004c6e00(0,0);
  FUN__text__004c6e50(*(undefined4 *)(local_8 + 0x9258),0,*(undefined4 *)(local_8 + 0x9254));
  local_8 = 0x4c5802;
  FUN__text__0056ce80();
  return;
}

