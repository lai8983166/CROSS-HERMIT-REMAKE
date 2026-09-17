
/* WARNING: Removing unreachable block (ram,0x0041c989) */

void FUN__text__0041c830(undefined4 param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_6c [16];
  int local_2c;
  int local_28;
  int local_24;
  undefined4 local_20;
  undefined1 local_1c [8];
  undefined4 local_14;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_6c;
  for (iVar2 = 0x1a; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_24 = FUN__text__0041a120(0);
  if (local_24 == -1) {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                DAT_005ff59c + 0x26,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else if (local_24 == 1) {
    do {
      while( true ) {
        while (local_28 = FUN__text__0041a1e0(local_1c), local_c = local_28, local_28 == -1) {
          iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                      DAT_005ff59c + 0x20,0);
          if (iVar2 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        if (local_28 != 0) break;
        iVar2 = FUN__text__00419450();
        if (iVar2 == 0) {
          local_c = FUN__text__0041ce60(param_1,local_1c);
        }
        else {
          local_c = FUN__text__0041c9d0(param_1,local_1c);
        }
        local_2c = local_c;
        if (local_c == -1) {
          iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                      DAT_005ff59c + 0x18,0);
          if (iVar2 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        else if (local_c == 1) {
          (*DAT_005923c4)(param_1,0);
          FUN__text__0056ce80();
        }
        local_20 = local_14;
        FUN__text__00428ad0(local_14);
      }
    } while (local_28 != 1);
    local_28 = 1;
    local_c = 1;
  }
  local_8 = 0x41c9c7;
  FUN__text__0056ce80();
  return;
}

