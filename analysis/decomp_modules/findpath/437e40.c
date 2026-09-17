
void __thiscall
FUN__text__00437e40(int param_1,ushort param_2,ushort param_3,ushort param_4,ushort param_5,
                   undefined4 *param_6,undefined4 param_7,undefined4 param_8)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined1 *local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0;
  *(undefined4 *)(param_1 + 0x14) = param_7;
  local_8 = param_1;
  iVar2 = FUN__text__0043bfa0((int)(short)param_4,(int)(short)param_5,
                              *(undefined4 *)(param_1 + 0x14));
  if (iVar2 == 0) {
    *(ushort *)(param_6 + 6) = param_4 & 0xff;
    *(ushort *)((int)param_6 + 0x1a) = param_5 & 0xff;
    *(undefined1 *)(param_6 + 7) = (undefined1)param_2;
    *(undefined1 *)((int)param_6 + 0x1d) = (undefined1)param_3;
    *(undefined2 *)((int)param_6 + 0x1e) = 0;
    *(undefined2 *)(param_6 + 8) = 1;
    *(undefined1 *)((int)param_6 + 0x22) = (undefined1)param_4;
    *(undefined1 *)((int)param_6 + 0x23) = (undefined1)param_5;
  }
  else {
    FUN__text__00439c60();
    local_c = FUN__text__004396e0();
    if (local_c == 0) {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",
                                  DAT_005ff9b0 + 0x24,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      *(ushort *)(param_6 + 6) = param_4;
      *(ushort *)((int)param_6 + 0x1a) = param_5;
    }
    else {
      local_10 = *(undefined1 **)(local_c + 8);
      *(ushort *)(local_10 + 2) = param_2 & 0xff;
      *(ushort *)(local_10 + 4) = param_3 & 0xff;
      *(undefined4 *)(local_10 + 0x14) = 0;
      *(undefined4 *)(local_10 + 8) = 0;
      *(int *)(local_10 + 0xc) =
           ((int)(short)param_4 - (int)(short)param_2) * ((int)(short)param_4 - (int)(short)param_2)
           + ((int)(short)param_5 - (int)(short)param_3) *
             ((int)(short)param_5 - (int)(short)param_3);
      *(int *)(local_10 + 0x10) = *(int *)(local_10 + 8) + *(int *)(local_10 + 0xc);
      FUN__text__00439790();
      *local_10 = 0x40;
      FUN__text__00439a90(local_c);
      FUN__text__004398d0((int)*(short *)(local_10 + 2),(int)*(short *)(local_10 + 4),local_c);
      *param_6 = *(undefined4 *)(local_8 + 0x5c);
      param_6[1] = *(undefined4 *)(local_8 + 0x60);
      param_6[2] = *(undefined4 *)(local_8 + 100);
      param_6[3] = *(undefined4 *)(local_8 + 0x68);
      param_6[4] = *(undefined4 *)(local_8 + 0x6c);
      param_6[5] = *(undefined4 *)(local_8 + 0x70);
      *(ushort *)(param_6 + 6) = param_4;
      *(ushort *)((int)param_6 + 0x1a) = param_5;
      local_1c = FUN__text__004380b0(param_6,param_8);
      local_18 = local_1c;
    }
  }
  local_8 = 0x4380a4;
  FUN__text__0056ce80();
  return;
}

