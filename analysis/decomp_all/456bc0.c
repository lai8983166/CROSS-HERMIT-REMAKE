
void __thiscall FUN__text__00456bc0(int param_1,int param_2)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  bool bVar5;
  undefined4 uVar6;
  undefined1 *puVar7;
  undefined4 local_14c [16];
  int local_10c;
  int local_108;
  int local_104;
  int *local_100;
  int *local_fc;
  int *local_f8;
  undefined1 local_f4 [188];
  int *local_38;
  int *local_34;
  int local_30;
  uint local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18 [2];
  int *local_10;
  int local_8;
  
  puVar4 = local_14c;
  for (iVar3 = 0x52; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  FUN__text__00416fa0(param_1 + 0x117e18);
  local_20 = 0;
  local_2c = 0;
  local_28 = 0;
  iVar3 = FUN__text__0041aea0();
  if (1 < iVar3) {
    do {
      FUN__text__00416fa0(local_8 + 0x117e38);
      local_1c = FUN__text__0041a120(1);
      FUN__text__00416ff0(local_8 + 0x117e38);
      FUN__text__00417050(local_8 + 0x117e38);
      bVar5 = CARRY4(local_2c,*(uint *)(local_8 + 0x117e50));
      local_2c = local_2c + *(uint *)(local_8 + 0x117e50);
      local_28 = local_28 + *(int *)(local_8 + 0x117e54) + (uint)bVar5;
      do {
        while( true ) {
          while (local_104 = FUN__text__0041a1e0(local_18), local_1c = local_104, local_104 == -1) {
            iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                        "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                        DAT_0060cdc4 + 0x1e,0);
            if (iVar3 != 0) {
              pcVar1 = (code *)swi(3);
              (*pcVar1)();
              return;
            }
          }
          if (local_104 != 0) break;
          if (local_18[0] == 0) {
            local_34 = local_10;
            local_108 = *local_10;
            if (local_108 == 5) {
              local_38 = local_10;
              local_30 = FUN__text__0041abf0(local_10[2]);
              if (local_30 != 0) {
                FUN__text__0056d810(local_f4,&DAT_0059a720,local_30 + 2);
                puVar7 = local_f4;
                uVar6 = 0xffffffff;
                uVar2 = FUN__text__0041ad60(0xffffffff,puVar7);
                FUN__text__00457e00(uVar2,uVar6,puVar7);
                FUN__text__004254c0(local_f4);
              }
              FUN__text__0041b0f0(local_38[2]);
            }
            else if (local_108 == 0x31) {
              local_fc = local_10;
              FUN__text__00428ad0(local_10);
              goto LAB__text__00456fef;
            }
          }
          else {
            local_f8 = local_10;
            if ((local_10[1] != -0x73607248) &&
               (iVar3 = FUN__text__00424f80("head->IdCode == 0x8C9F8DB8",
                                            "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                            DAT_0060cdc4 + 0x56,0), iVar3 != 0)) {
              pcVar1 = (code *)swi(3);
              (*pcVar1)();
              return;
            }
            local_10c = *(byte *)((int)local_f8 + 0xd) - 1;
            switch(*(byte *)((int)local_f8 + 0xd)) {
            case 1:
            case 2:
            case 3:
            case 5:
            case 6:
            case 7:
            case 8:
            case 9:
            case 10:
            case 0xc:
            case 0xd:
            case 0xe:
              break;
            case 4:
              if ((param_2 != 0) &&
                 (iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                              "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp"
                                              ,DAT_0060cdc4 + 0x5b,0), iVar3 != 0)) {
                pcVar1 = (code *)swi(3);
                (*pcVar1)();
                return;
              }
              FUN__text__0048d490(local_10);
              local_20 = local_20 + 1;
              break;
            case 0xb:
              FUN__text__00457f50(local_18);
              break;
            case 0xf:
              if ((param_2 == 0) &&
                 (iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                              "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp"
                                              ,DAT_0060cdc4 + 0x6e,0), iVar3 != 0)) {
                pcVar1 = (code *)swi(3);
                (*pcVar1)();
                return;
              }
              local_20 = local_20 + 1;
              break;
            case 0x10:
              FUN__text__00458450(local_18);
              break;
            default:
              iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                          "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                          DAT_0060cdc4 + 0x85,0);
              if (iVar3 != 0) {
                pcVar1 = (code *)swi(3);
                (*pcVar1)();
                return;
              }
            }
          }
          local_100 = local_10;
          FUN__text__00428ad0(local_10);
        }
      } while (local_104 != 1);
      local_24 = FUN__text__0041aea0();
      local_24 = local_24 + -1;
    } while (local_20 != local_24);
  }
  *(uint *)(local_8 + 0x117e50) = local_2c;
  *(int *)(local_8 + 0x117e54) = local_28;
  FUN__text__00416ff0(local_8 + 0x117e18);
  FUN__text__00417050(local_8 + 0x117e18);
LAB__text__00456fef:
  local_8 = 0x456fff;
  FUN__text__0056ce80();
  return;
}

