
void __thiscall FUN__text__0047bed0(int param_1,int param_2,uint param_3)

{
  code *pcVar1;
  undefined1 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_60 [16];
  uint local_20;
  undefined4 local_1c;
  ushort local_18;
  ushort local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar4 = local_60;
  for (iVar3 = 0x17; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_20 = param_3 & 0xff;
  local_8 = param_1;
  switch(local_20) {
  case 0:
  case 5:
    iVar3 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e50 + 9,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    goto switchD__text__0047bf05_default;
  case 1:
  case 2:
  case 3:
    iVar3 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10);
    local_c = (short)((int)(iVar3 + (iVar3 >> 0x1f & 0x1fU)) >> 5);
    iVar3 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10);
    local_10 = (short)((int)(iVar3 + (iVar3 >> 0x1f & 0xfU)) >> 4);
    iVar3 = *(int *)(param_1 + 0x80dd8 + *(short *)(param_2 + 0x4ee) * 0x520);
    local_14 = (ushort)((int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0x1fU)) >> 5);
    iVar3 = *(int *)(param_1 + 0x80ddc + *(short *)(param_2 + 0x4ee) * 0x520);
    local_18 = (ushort)((int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0xfU)) >> 4);
    uVar2 = FUN__text__004ddc60(param_2,(int)*(short *)(param_2 + 0x4f2));
    local_1c = CONCAT31(local_1c._1_3_,uVar2);
    iVar3 = FUN__text__0043c1d0((int)local_c,(int)local_10,(int)(short)local_14,(int)(short)local_18
                                ,uVar2);
    break;
  case 4:
    iVar3 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10);
    local_c = (short)((int)(iVar3 + (iVar3 >> 0x1f & 0x1fU)) >> 5);
    iVar3 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10);
    local_10 = (short)((int)(iVar3 + (iVar3 >> 0x1f & 0xfU)) >> 4);
    local_14 = (ushort)*(byte *)(param_2 + 0x4f0);
    local_18 = (ushort)*(byte *)(param_2 + 0x4f1);
    uVar2 = FUN__text__004ddc60(param_2,(int)*(short *)(param_2 + 0x4f2));
    local_1c = CONCAT31(local_1c._1_3_,uVar2);
    iVar3 = FUN__text__0043c1d0((int)local_c,(int)local_10,(int)(short)local_14,(int)(short)local_18
                                ,uVar2);
    break;
  case 6:
    iVar3 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10);
    local_c = (short)((int)(iVar3 + (iVar3 >> 0x1f & 0x1fU)) >> 5);
    iVar3 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10);
    local_10 = (short)((int)(iVar3 + (iVar3 >> 0x1f & 0xfU)) >> 4);
    iVar3 = *(int *)(param_1 + 0x80dd8 + *(short *)(param_2 + 0x4ee) * 0x520);
    local_14 = (ushort)((int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0x1fU)) >> 5);
    iVar3 = *(int *)(param_1 + 0x80ddc + *(short *)(param_2 + 0x4ee) * 0x520);
    local_18 = (ushort)((int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0xfU)) >> 4);
    uVar2 = FUN__text__004ddc60(param_2,(int)*(short *)(param_2 + 0x4f2));
    local_1c = CONCAT31(local_1c._1_3_,uVar2);
    iVar3 = FUN__text__0043c1d0((int)local_c,(int)local_10,(int)(short)local_14,(int)(short)local_18
                                ,uVar2);
    break;
  default:
    goto switchD__text__0047bf05_default;
  }
  if (iVar3 == 0) {
switchD__text__0047bf05_default:
    iVar3 = FUN__text__004698a0(param_2);
    if (iVar3 != 0) {
      FUN__text__00469950(param_2);
    }
  }
  local_8 = 0x47c1e2;
  FUN__text__0056ce80();
  return;
}

