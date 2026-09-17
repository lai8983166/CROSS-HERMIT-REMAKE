
void __thiscall FUN__text__0047c210(int param_1,int param_2,uint param_3)

{
  code *pcVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  uint local_24;
  char local_20;
  char local_1c;
  ushort local_18;
  ushort local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_24 = param_3 & 0xff;
  local_8 = param_1;
  switch(local_24) {
  case 0:
  case 5:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e54 + 8,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    break;
  case 1:
  case 2:
  case 3:
    iVar2 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10);
    local_c = (short)((int)(iVar2 + (iVar2 >> 0x1f & 0x1fU)) >> 5);
    iVar2 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10);
    local_10 = (short)((int)(iVar2 + (iVar2 >> 0x1f & 0xfU)) >> 4);
    iVar2 = *(int *)(param_1 + 0x80dd8 + *(short *)(param_2 + 0x4ee) * 0x520);
    local_14 = (ushort)((int)((iVar2 >> 0x10) + (iVar2 >> 0x1f & 0x1fU)) >> 5);
    iVar2 = *(int *)(param_1 + 0x80ddc + *(short *)(param_2 + 0x4ee) * 0x520);
    local_18 = (ushort)((int)((iVar2 >> 0x10) + (iVar2 >> 0x1f & 0xfU)) >> 4);
    local_1c = FUN__text__004ddbb0(param_2);
    iVar2 = FUN__text__0043c1d0((int)local_c,(int)local_10,(int)(short)local_14,(int)(short)local_18
                                ,(int)local_1c);
    if ((iVar2 == 0) && (iVar2 = FUN__text__00468d80(param_2), iVar2 != 0)) {
      FUN__text__0047e460(param_2,local_14,CONCAT22(extraout_var,local_18));
    }
    break;
  case 4:
    iVar2 = FUN__text__00468d80(param_2);
    if ((iVar2 == 0) && (*(char *)(*(int *)(param_2 + 600) + 0x9f) == '\x02')) {
      local_20 = FUN__text__004ddc60(param_2,(int)*(short *)(param_2 + 0x4f2));
      local_c = (short)((int)((*(int *)(param_2 + 0x2ec) >> 0x10) +
                             (*(int *)(param_2 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
      local_10 = (short)((int)((*(int *)(param_2 + 0x2f0) >> 0x10) +
                              (*(int *)(param_2 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
      local_14 = (ushort)*(byte *)(param_2 + 0x4f0);
      local_18 = (ushort)*(byte *)(param_2 + 0x4f1);
      FUN__text__0043c1d0((int)local_c,(int)local_10,local_14,local_18,(int)local_20);
    }
    break;
  case 6:
    iVar2 = FUN__text__00468d80(param_2);
    if (iVar2 == 0) {
      iVar2 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10);
      local_c = (short)((int)(iVar2 + (iVar2 >> 0x1f & 0x1fU)) >> 5);
      iVar2 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10);
      local_10 = (short)((int)(iVar2 + (iVar2 >> 0x1f & 0xfU)) >> 4);
      iVar2 = *(int *)(local_8 + 0x80dd8 + *(short *)(param_2 + 0x4ee) * 0x520);
      local_14 = (ushort)((int)((iVar2 >> 0x10) + (iVar2 >> 0x1f & 0x1fU)) >> 5);
      iVar2 = *(int *)(local_8 + 0x80ddc + *(short *)(param_2 + 0x4ee) * 0x520);
      local_18 = (ushort)((int)((iVar2 >> 0x10) + (iVar2 >> 0x1f & 0xfU)) >> 4);
      local_1c = FUN__text__004ddbb0(param_2);
      FUN__text__0043c1d0((int)local_c,(int)local_10,(int)(short)local_14,(int)(short)local_18,
                          (int)local_1c);
    }
  }
  local_8 = 0x47c553;
  FUN__text__0056ce80();
  return;
}

