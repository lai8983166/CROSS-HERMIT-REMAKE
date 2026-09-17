
void __fastcall FUN__text__00448650(int param_1)

{
  undefined2 uVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_78 [16];
  int local_38;
  undefined4 local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  undefined4 local_20;
  int local_1c;
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_78;
  for (iVar3 = 0x1d; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_18 = param_1 + 0x1a54;
  local_8 = param_1;
  uVar2 = FUN__text__00571020(0);
  FUN__text__00570fd0(uVar2);
  FUN__text__0044baa0();
  FUN__text__00448920();
  uVar1 = FUN__text__0044c270((int)*(short *)(local_8 + 0x1a88));
  *(undefined2 *)(local_8 + 0x1aa4) = uVar1;
  *(undefined1 *)(local_8 + 0x1a90) = 0;
  _memset((void *)(local_8 + 0x1a91),0,4);
  local_20 = 0;
  local_2c = 10;
  local_30 = 0;
  _memset((void *)(local_8 + 0x1bb0),0,0x10);
  local_10 = 0;
  local_c = 1;
  do {
    if (local_c == 0) {
      local_8 = 0x448906;
      FUN__text__0056ce80();
      return;
    }
    local_34 = *(undefined4 *)(local_8 + 0x1bb0);
    switch(local_34) {
    case 0:
      local_14 = FUN__text__00442090();
      if (local_14 == 0) {
        iVar3 = FUN__text__00419450();
        if (iVar3 == 0) {
          *(undefined4 *)(local_8 + 0x1bb0) = 3;
        }
        else {
          *(undefined4 *)(local_8 + 0x1bb0) = 1;
        }
      }
      else if (local_30 < local_2c) {
        local_30 = local_30 + 1;
      }
      else {
        *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
      }
      break;
    case 1:
      local_28 = FUN__text__0041aea0();
      local_24 = 0;
      for (local_1c = 0; local_1c != 4; local_1c = local_1c + 1) {
        local_24 = local_24 + *(char *)(local_8 + local_1c + 0x1a91);
      }
      if (local_24 == local_28) {
        local_30 = 0;
        *(undefined4 *)(local_8 + 0x1bb0) = 2;
      }
      break;
    case 2:
      local_14 = FUN__text__00442360();
      if (local_14 != 0) {
        if (local_30 < local_2c) {
          local_30 = local_30 + 1;
        }
        else {
          *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
        }
        break;
      }
      goto LAB__text__00448899;
    case 3:
      if (*(char *)(local_8 + 0x1a90) != '\0') goto LAB__text__00448899;
    }
    iVar3 = FUN__text__00419450();
    if (iVar3 == 0) {
      local_14 = FUN__text__00448e50();
    }
    else {
      local_14 = FUN__text__00448cc0();
    }
    local_38 = local_14;
    if (local_14 == 2) {
LAB__text__00448899:
      FUN__text__00448a30();
      *(undefined4 *)(local_8 + 0x1a50) = 4;
      local_10 = 1;
      local_c = 0;
    }
    else if (local_14 == 3) {
      *(undefined4 *)(local_8 + 0x1a50) = 2;
      local_10 = 2;
      local_c = 0;
    }
    FUN__text__0044ca80();
    FUN__text__00422360(0);
  } while( true );
}

