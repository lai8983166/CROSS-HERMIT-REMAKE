
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__00446780(int param_1)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  undefined1 local_18 [4];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_60;
  for (iVar3 = 0x17; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  _DAT_007a3f9c = 0;
  local_14 = param_1 + 0x1a54;
  *(undefined4 *)(param_1 + 0x1bc8) = 0;
  local_8 = param_1;
  FUN__text__00446e20();
  _memset((void *)(local_8 + 0x1bb0),0,0x10);
  local_10 = 1;
  do {
    if (local_10 == 0) {
      local_8 = 0x446a5f;
      FUN__text__0056ce80();
      return;
    }
    local_1c = *(int *)(local_8 + 0x1bb0);
    if (local_1c == 0) {
      local_c = FUN__text__0044c710(&DAT_00605bb8,4);
      if ((local_c != -1) && ((*(uint *)(DAT_007a49fc + 0x199c) & 1) != 0)) {
        local_20 = local_c;
        switch(local_c) {
        case 0:
          local_c = -1;
          break;
        case 1:
          FUN__text__004db2b0(5);
          iVar3 = FUN__text__00446fa0();
          if (iVar3 == 0) {
            *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
            *(undefined4 *)(local_8 + 0x1bc4) = 6;
          }
          else {
            uVar2 = FUN__text__00446e90();
            *(undefined4 *)(DAT_007a4a00 + 0x110c) = uVar2;
            *(undefined4 *)(local_8 + 0x1a50) = 7;
            local_10 = 0;
          }
          break;
        case 2:
          *(undefined4 *)(local_8 + 0x1bb0) = 1;
          *(undefined4 *)(local_8 + 0x1bb4) = 0;
          FUN__text__004db2b0(5);
          break;
        case 3:
          FUN__text__004db2b0(2);
          *(undefined4 *)(local_8 + 0x1a50) = 2;
          local_10 = 0;
          break;
        default:
          iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                      DAT_0060672c + 0x39,0);
          if (iVar3 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
      }
      FUN__text__004470c0();
      FUN__text__00447660(0xff);
      if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) == 0) {
        local_c = -1;
      }
      FUN__text__00446c70(local_c,0xff);
      FUN__text__0044ca80();
      FUN__text__0044c9a0(0);
    }
    else if (local_1c == 1) {
      iVar3 = FUN__text__00446a80();
      if (iVar3 != 0) {
        local_10 = 0;
      }
      FUN__text__00447660(0xff);
    }
    else if (local_1c == 0xff) {
      iVar3 = FUN__text__00441630(*(undefined4 *)(local_8 + 0x1bc4),local_18,0x200,0x180,0x3c);
      if (iVar3 != 0) {
        if (*(int *)(local_8 + 0x1bc8) == 0) {
          *(undefined4 *)(local_8 + 0x1bb0) = 0;
        }
        else {
          *(undefined4 *)(local_8 + 0x1a50) = 2;
          local_10 = 0;
        }
      }
      FUN__text__00447660(0x40);
      FUN__text__00446c70(0xffffffff,0x40);
      FUN__text__0044ca80();
      FUN__text__0044c9a0(0);
    }
    FUN__text__00422360(0);
  } while( true );
}

