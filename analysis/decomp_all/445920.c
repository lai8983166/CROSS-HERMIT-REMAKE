
/* WARNING: Removing unreachable block (ram,0x00445b22) */

void __fastcall FUN__text__00445920(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  undefined4 local_28;
  int local_24;
  int local_20;
  undefined4 local_1c;
  undefined2 local_18;
  undefined2 local_14;
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  local_1c = *(undefined4 *)(param_1 + 0x1bb4);
  local_8 = param_1;
  switch(local_1c) {
  case 0:
    FUN__text__00445eb0(param_1 + 0x8a50,param_1 + 0x8a58);
    *(undefined4 *)(local_8 + 0x1bc0) = 1;
    FUN__text__0040d390(0x13,0,0xffffffff,0);
    *(int *)(local_8 + 0x1bb4) = *(int *)(local_8 + 0x1bb4) + 1;
    break;
  case 1:
    if (*(int *)(param_1 + 0x1bc0) == 0) {
      FUN__text__004188b0();
      *(undefined4 *)(local_8 + 0x1bc0) = 0;
      *(int *)(local_8 + 0x1bb4) = *(int *)(local_8 + 0x1bb4) + 1;
    }
    else {
      *(int *)(param_1 + 0x1bc0) = *(int *)(param_1 + 0x1bc0) + -1;
    }
    break;
  case 2:
  case 3:
  case 4:
    local_20 = FUN__text__00418900();
    if (local_20 == 0) {
      *(int *)(local_8 + 0x1bc0) = *(int *)(local_8 + 0x1bc0) + 1;
    }
    else if (local_20 != 1) {
      *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
      *(undefined4 *)(local_8 + 0x1bc4) = 2;
    }
    local_10 = local_20;
    if (0x169 < *(int *)(local_8 + 0x1bc0)) {
      if (*(int *)(local_8 + 0x1a54) == 0) {
        *(undefined4 *)(local_8 + 0x1bb4) = 5;
      }
      else {
        local_24 = *(int *)(local_8 + 0x1bb4);
        if (1 < local_24) {
          if (local_24 < 4) {
            FUN__text__0040d390(0x13,0,0xffffffff,0);
            *(undefined4 *)(local_8 + 0x1bc0) = 0;
            *(int *)(local_8 + 0x1bb4) = *(int *)(local_8 + 0x1bb4) + 1;
          }
          else if (local_24 == 4) {
            *(undefined4 *)(local_8 + 0x1bb4) = 5;
          }
        }
      }
    }
    break;
  case 5:
    local_10 = 0;
    local_28 = 0;
    FUN__text__00445f00(param_1 + 0x8a50);
    FUN__text__00445f60(local_8 + 0x8a50,local_8 + 0x8a58);
    *(undefined4 *)(local_8 + 0x1bb0) = 0;
  }
  local_14 = 0x1be;
  local_18 = 0x157;
  FUN__text__0040ec50(0x1be,0x157,0x58,0xffffffff,0,"Now Search...");
  FUN__text__00446340(0xffffffff,0xff);
  FUN__text__0044ca80();
  FUN__text__0044c9a0(0);
  local_8 = 0x445bea;
  FUN__text__0056ce80();
  return;
}

