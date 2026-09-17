
void __thiscall FUN__text__0043a640(int param_1,int param_2)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_160 [16];
  undefined4 local_120;
  undefined4 local_11c;
  undefined4 local_118;
  undefined4 local_114;
  undefined4 local_110;
  undefined1 local_10c [260];
  int local_8;
  
  puVar4 = local_160;
  for (iVar3 = 0x57; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 0x2659c) != 0) {
    local_110 = *(undefined4 *)(param_1 + 0x2659c);
    FUN__text__00428ad0(local_110);
    *(undefined4 *)(local_8 + 0x2659c) = 0;
  }
  if (*(int *)(local_8 + 0x265a0) != 0) {
    if (**(int **)(local_8 + 0x265a0) != 0) {
      local_114 = **(undefined4 **)(local_8 + 0x265a0);
      FUN__text__00428ad0(local_114);
      **(undefined4 **)(local_8 + 0x265a0) = 0;
    }
    local_118 = *(undefined4 *)(local_8 + 0x265a0);
    FUN__text__00428ad0(local_118);
    *(undefined4 *)(local_8 + 0x265a0) = 0;
  }
  FUN__text__0056d810(local_10c,&DAT_00592b28,"data\\tactics\\map\\",
                      (&PTR_s_map00_bin_006b13f0)[param_2 * 4]);
  uVar2 = FUN__text__004500b0(local_10c);
  uVar2 = FUN__text__0042ae20(uVar2);
  *(undefined4 *)(local_8 + 0x2659c) = uVar2;
  if ((*(int *)(local_8 + 0x2659c) == 0) &&
     (iVar3 = FUN__text__00424f80("MapCw!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ff9d4 + 0xe,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(int *)(local_8 + 0x2659c) != 0) {
    local_11c = FUN__text__00428a40(4);
    *(undefined4 *)(local_8 + 0x265a0) = local_11c;
    if ((*(int *)(local_8 + 0x265a0) == 0) &&
       (iVar3 = FUN__text__00424f80("MapCm!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                    DAT_005ff9d4 + 0x26,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    _memset(*(void **)(local_8 + 0x265a0),0,4);
    local_120 = FUN__text__00428a40((int)*(short *)(*(int *)(local_8 + 0x2659c) + 4) *
                                    (int)*(short *)(*(int *)(local_8 + 0x2659c) + 6) * 2);
    **(undefined4 **)(local_8 + 0x265a0) = local_120;
    if ((**(int **)(local_8 + 0x265a0) == 0) &&
       (iVar3 = FUN__text__00424f80("MapCm->data!=0",
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                    DAT_005ff9d4 + 0x29,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    _memset((void *)**(undefined4 **)(local_8 + 0x265a0),0,
            *(short *)(*(int *)(local_8 + 0x2659c) + 4) * 2 *
            (int)*(short *)(*(int *)(local_8 + 0x2659c) + 6));
    FUN__text__0043ce10();
    *(undefined2 *)(local_8 + 0x265a4) = (undefined2)param_2;
    *(undefined2 *)(local_8 + 0x265a8) = 0;
    *(undefined2 *)(local_8 + 0x265a6) = 0;
    *(undefined2 *)(local_8 + 0x265a6) = 0x3a0;
    *(undefined2 *)(local_8 + 0x265a8) = 0;
    *(undefined2 *)(local_8 + 0x265a6) = 0;
    *(undefined2 *)(local_8 + 0x265a8) = 0;
  }
  local_8 = 0x43a91a;
  FUN__text__0056ce80();
  return;
}

