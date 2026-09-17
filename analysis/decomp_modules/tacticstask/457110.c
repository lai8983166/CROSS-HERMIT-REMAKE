
void __thiscall FUN__text__00457110(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  bool bVar4;
  undefined4 local_84 [16];
  int local_44;
  int local_40;
  int local_3c;
  int *local_38;
  int *local_34;
  int *local_30;
  uint local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c [2];
  int *local_14;
  int *local_c;
  int local_8;
  
  puVar3 = local_84;
  for (iVar2 = 0x20; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  FUN__text__00416fa0(param_1 + 0x117e78);
  local_2c = 0;
  local_28 = 0;
  local_24 = 0;
  do {
    FUN__text__00416fa0(local_8 + 0x117e98);
    local_20 = FUN__text__0041a120(1);
    FUN__text__00416ff0(local_8 + 0x117e98);
    FUN__text__00417050(local_8 + 0x117e98);
    bVar4 = CARRY4(local_2c,*(uint *)(local_8 + 0x117eb0));
    local_2c = local_2c + *(uint *)(local_8 + 0x117eb0);
    local_28 = local_28 + *(int *)(local_8 + 0x117eb4) + (uint)bVar4;
    do {
      while( true ) {
        while (local_3c = FUN__text__0041a1e0(local_1c), local_20 = local_3c, local_3c == -1) {
          iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                      DAT_0060cdcc + 0x1c,0);
          if (iVar2 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        if (local_3c != 0) break;
        if (local_1c[0] == 0) {
          local_c = local_14;
          local_40 = *local_14;
          if ((local_40 != 5) && (local_40 != 0x31)) goto LAB__text__004573ab;
LAB__text__0045726e:
          local_34 = local_14;
          FUN__text__00428ad0(local_14);
          goto LAB__text__00457406;
        }
        local_30 = local_14;
        local_44 = *(byte *)((int)local_14 + 0xd) - 4;
        switch(*(byte *)((int)local_14 + 0xd)) {
        case 4:
          if ((param_2 != 0) &&
             (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                          "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                          DAT_0060cdcc + 0x34,0), iVar2 != 0)) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
          if (local_1c[0] == 1) {
            local_24 = 1;
            local_30 = local_14;
            FUN__text__0048d280(local_14);
          }
          else {
            iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                        "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                        DAT_0060cdcc + 0x3c,0);
            if (iVar2 != 0) {
              pcVar1 = (code *)swi(3);
              (*pcVar1)();
              return;
            }
          }
          break;
        default:
          goto LAB__text__0045726e;
        case 0xb:
          FUN__text__00457f50(local_1c);
          break;
        case 0xf:
          if ((param_2 == 0) &&
             (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                          "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                          DAT_0060cdcc + 0x49,0), iVar2 != 0)) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
          local_24 = 1;
          break;
        case 0x10:
          FUN__text__00458450(local_1c);
        }
LAB__text__004573ab:
        local_38 = local_14;
        FUN__text__00428ad0(local_14);
      }
    } while (local_3c != 1);
    if (local_24 != 0) {
      *(uint *)(local_8 + 0x117eb0) = local_2c;
      *(int *)(local_8 + 0x117eb4) = local_28;
      FUN__text__00416ff0(local_8 + 0x117e78);
      FUN__text__00417050(local_8 + 0x117e78);
LAB__text__00457406:
      local_8 = 0x457416;
      FUN__text__0056ce80();
      return;
    }
    local_20 = 1;
  } while( true );
}

