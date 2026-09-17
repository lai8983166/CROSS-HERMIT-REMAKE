
void FUN__text__0043a920(int param_1)

{
  code *pcVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 local_158 [16];
  int local_118;
  int local_114;
  undefined1 local_110 [260];
  int local_c;
  int local_8;
  
  puVar5 = local_158;
  for (iVar4 = 0x55; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  FUN__text__00407780();
  FUN__text__0056d810(local_110,&DAT_00592b28,"data\\tactics\\map\\",
                      (&PTR_s_map00_map_006b13f4)[param_1 * 4]);
  uVar2 = FUN__text__004500b0(local_110);
  local_114 = FUN__text__0042ae20(uVar2);
  if ((local_114 == 0) &&
     (iVar4 = FUN__text__00424f80("gmp!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ff9d8 + 0x13,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  *(undefined4 *)(local_8 + 0x263b4) = 0x5c;
  local_c = FUN__text__004167e0(local_114 + 0x404,*(undefined4 *)(local_8 + 0x263b4),0);
  if (local_c == 0) {
    local_118 = local_114;
    FUN__text__00428ad0(local_114);
    FUN__text__00407780();
    FUN__text__0056d810(local_110,&DAT_00592b28,"data\\tactics\\map\\",
                        (&PTR_s_map00_bmp_006b13f8)[param_1 * 4]);
    uVar7 = 1;
    uVar6 = 1;
    uVar2 = FUN__text__004500b0(local_110);
    uVar3 = FUN__text__004142b0(uVar2,uVar6,uVar7);
    local_c = FUN__text__00404b40(uVar3,uVar2,uVar6,uVar7);
    if ((local_c == 1) &&
       (iVar4 = FUN__text__00424f80("ret!=1","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                    DAT_005ff9d8 + 0x34,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (local_c == 0) {
      FUN__text__004404a0((int)*(short *)(*(int *)(local_8 + 0x2659c) + 4) << 5,
                          (int)*(short *)(*(int *)(local_8 + 0x2659c) + 6) << 4);
    }
  }
  local_8 = 0x43aaff;
  FUN__text__0056ce80();
  return;
}

