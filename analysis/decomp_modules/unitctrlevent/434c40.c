
void FUN__text__00434c40(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  short local_28;
  short local_24;
  short local_20;
  undefined4 local_1c;
  int local_18;
  undefined4 local_14;
  uint local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_68;
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__00499200();
  FUN__text__00499240(1);
  FUN__text__00499240(2);
  FUN__text__00499240(3);
  FUN__text__00499240(4);
  FUN__text__00499240(5);
  FUN__text__00499240(6);
  FUN__text__00499240(7);
  FUN__text__00499240(8);
  FUN__text__00499240(9);
  FUN__text__00499240(10);
  FUN__text__00499240(0xb);
  FUN__text__00499240(0xc);
  local_1c = FUN__text__00431d40(0x2d);
  iVar2 = FUN__text__00469220(local_1c);
  if (iVar2 != 0) {
    FUN__text__00499240(0xe);
  }
  local_1c = FUN__text__00431d40(0x2e);
  iVar2 = FUN__text__00469220(local_1c);
  if (iVar2 != 0) {
    FUN__text__00499240(0xf);
  }
  local_18 = FUN__text__00499280();
  if (local_18 != 0xffff) {
    FUN__text__00498e60(local_18);
    FUN__text__00498db0(local_18,3,1);
    FUN__text__00498db0(local_18,1,0);
    local_10 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent017.cpp",
                                   DAT_005ff7f8 + 0x34);
    local_10 = local_10 & 0x80000003;
    if ((int)local_10 < 0) {
      local_10 = (local_10 - 1 | 0xfffffffc) + 1;
    }
    FUN__text__00498db0(local_18,2,(int)(char)(&DAT_005ff7e7)[local_10 * 4]);
    local_20 = (short)(char)(&DAT_005ff7e4)[local_10 * 4];
    local_24 = (short)(char)(&DAT_005ff7e5)[local_10 * 4];
    local_28 = (short)(char)(&DAT_005ff7e6)[local_10 * 4];
    FUN__text__004988d0(local_18,(int)local_20,(int)local_24,(int)local_28);
  }
  iVar2 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent017.cpp",
                              DAT_005ff7f8 + 0x70);
  local_c = iVar2 % 0x3f48 + 0x708;
  if ((local_c < 1) &&
     (iVar2 = FUN__text__00424f80("0 < time",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent017.cpp",
                                  DAT_005ff7f8 + 0x73,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_14 = FUN__text__004554c0();
  FUN__text__00498fc0(local_14,0,0x14,local_c);
  local_8 = 0x434e8a;
  FUN__text__0056ce80();
  return;
}

