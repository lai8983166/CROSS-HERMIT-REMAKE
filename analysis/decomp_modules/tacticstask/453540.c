
void __fastcall FUN__text__00453540(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18;
  undefined4 local_14;
  int local_10;
  undefined *local_c;
  int local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0xf9;
  local_c = (&PTR_DAT_006a7f6c)[DAT_007f4488];
  local_18 = (int)*(short *)(&DAT_006a85ac + DAT_007f4488 * 2);
  local_20 = 0;
  local_1c = 0xf9;
  local_8 = param_1;
  do {
    if (local_20 == local_18) {
      local_8 = 0x45364a;
      FUN__text__0056ce80();
      return;
    }
    local_10 = local_8 + 0xd0dbc + local_1c * 0xb0;
    if (*(short *)(local_8 + 0x80c7c + local_1c * 0x520) != 0) {
      iVar2 = FUN__text__00424f80("UnitCt.uw[i].used == 0",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                  DAT_0060cd7c + 0x16,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    FUN__text__004da450(local_c + local_20 * 0x54,local_10);
    FUN__text__004680b0(local_1c);
    FUN__text__00451d80();
    local_20 = local_20 + 1;
    local_1c = local_1c + -1;
  } while( true );
}

