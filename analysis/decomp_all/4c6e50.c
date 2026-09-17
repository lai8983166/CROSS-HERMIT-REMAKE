
void FUN__text__004c6e50(undefined4 param_1,int param_2,uint param_3)

{
  uint uVar1;
  undefined1 uVar2;
  int iVar3;
  undefined2 extraout_var;
  undefined4 *puVar4;
  undefined4 local_5c [16];
  undefined4 local_1c;
  uint local_18;
  undefined1 local_14;
  uint local_10;
  short local_c;
  byte *local_8;
  
  puVar4 = local_5c;
  for (iVar3 = 0x16; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar2 = FUN__text__004c7070();
  local_10 = CONCAT31(local_10._1_3_,uVar2);
  local_14 = FUN__text__004c70a0();
  uVar1 = local_18 >> 8;
  local_18 = local_18 & 0xffffff00;
  if (param_2 != -1) {
    *(undefined2 *)(local_8 + 10) = (undefined2)param_2;
  }
  if (param_3 != *(ushort *)(local_8 + (local_10 & 0xff) * 2 + 0xe)) {
    local_18 = CONCAT31((int3)uVar1,1);
  }
  local_1c = param_1;
  switch(param_1) {
  case 0:
    local_18 = local_18 & 0xffffff00;
    FUN__text__004c7030(0);
    break;
  case 1:
    FUN__text__004c7030(0);
    break;
  case 2:
  case 4:
    FUN__text__004c7030(0x3c);
    break;
  case 3:
  case 5:
    FUN__text__004c7030(0x3c);
    break;
  case 6:
    if (local_8[8] == 0) {
      param_1 = 2;
      FUN__text__004c7030(0x3c);
    }
    else {
      FUN__text__004c7030(0x3c);
      FUN__text__004c70e0();
      uVar2 = FUN__text__004c7070();
      local_10 = CONCAT31(local_10._1_3_,uVar2);
    }
  }
  local_8[8] = (byte)param_1;
  if ((local_18 & 0xff) != 0) {
    *(undefined2 *)(local_8 + (local_10 & 0xff) * 2 + 0xe) = (undefined2)param_3;
    local_c = ((ushort)local_10 & 0xff) + 0x30 + (ushort)*local_8 * 2;
    FUN__text__004cd7b0("data\\adv\\bin\\",&DAT_007a4bbc);
    FUN__text__004cd810(&DAT_007a4bbc,
                        (&PTR_s_dammy_bin_00621bbc)
                        [*(ushort *)(local_8 + (local_10 & 0xff) * 2 + 0xe)]);
    FUN__text__004cde10(&DAT_007a4bbc,CONCAT22(extraout_var,local_c));
  }
  local_8 = (byte *)0x4c6fff;
  FUN__text__0056ce80();
  return;
}

