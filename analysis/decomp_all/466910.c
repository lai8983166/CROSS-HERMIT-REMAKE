
void __fastcall FUN__text__00466910(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  char local_20;
  short local_1c;
  short local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0;
  local_8 = param_1;
  do {
    if (local_14 == 10) {
      local_8 = 0x466aa7;
      FUN__text__0056ce80();
      return;
    }
    local_c = local_8 + 0x10c680 + local_14 * 0x520;
    local_20 = *(char *)(local_c + 5);
    if (local_20 == '\0') {
      local_18 = (short)((uint)*(undefined4 *)(local_c + 0x2ec) >> 0x10) -
                 *(short *)(local_8 + 0x2a30e);
      local_1c = ((short)((uint)*(undefined4 *)(local_c + 0x2f0) >> 0x10) -
                 *(short *)(local_8 + 0x2a310)) + 0x1e;
    }
    else if (local_20 == '\x01') {
      local_18 = (short)((uint)*(undefined4 *)(local_c + 0x2ec) >> 0x10);
      local_1c = (short)((uint)*(undefined4 *)(local_c + 0x2f0) >> 0x10);
    }
    else if (local_20 == '\x02') {
      local_10 = local_8 + 0x80aec + *(short *)(local_c + 0xe) * 0x520;
      local_18 = (short)((uint)*(undefined4 *)(local_10 + 0x2ec) >> 0x10) -
                 *(short *)(local_8 + 0x2a30e);
      local_1c = ((short)((uint)*(undefined4 *)(local_10 + 0x2f0) >> 0x10) -
                 *(short *)(local_8 + 0x2a310)) + 0x1e;
    }
    else {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b28 + 0x17,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    FUN__text__0040a330(local_c + 0x48,local_8 + 0xde4b0,(int)local_18,(int)local_1c,
                        *(undefined2 *)(local_c + 0xc));
    local_14 = local_14 + 1;
  } while( true );
}

