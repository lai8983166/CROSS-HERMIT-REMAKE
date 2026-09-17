
void FUN__text__0041b200(undefined4 param_1,undefined4 param_2,uint *param_3)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_8c [16];
  uint local_4c;
  uint *local_48;
  uint *local_44;
  uint *local_40;
  uint *local_3c;
  uint *local_38;
  uint *local_34;
  uint *local_30;
  uint *local_2c;
  uint *local_28;
  uint *local_24;
  uint *local_20;
  uint *local_1c;
  uint *local_18;
  uint *local_14;
  uint *local_10;
  uint *local_c;
  uint *local_8;
  
  puVar3 = local_8c;
  for (iVar2 = 0x22; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_3;
  local_4c = *param_3;
  if (local_4c < 0x105) {
    if (local_4c == 0x104) {
      local_44 = param_3;
      FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_SETSESSIONDESC\n");
      uVar1 = local_4c;
    }
    else if (local_4c < 0x32) {
      if (local_4c == 0x31) {
        local_34 = param_3;
        FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_SESSIONLOST\n");
        uVar1 = local_4c;
      }
      else {
        uVar1 = local_4c - 3;
        switch(local_4c) {
        case 3:
          local_18 = param_3;
          local_4c = uVar1;
          FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_CREATEPLAYERORGROUP\n");
          uVar1 = local_4c;
          break;
        case 5:
          local_24 = param_3;
          local_4c = uVar1;
          FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_DESTROYPLAYERORGROUP\n");
          uVar1 = local_4c;
          break;
        case 7:
          local_10 = param_3;
          local_4c = uVar1;
          FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_ADDPLAYERTOGROUP\n");
          uVar1 = local_4c;
          break;
        case 0x21:
          local_20 = param_3;
          local_4c = uVar1;
          FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_DELETEPLAYERFROMGROUP\n");
          uVar1 = local_4c;
        }
      }
    }
    else if (local_4c == 0x101) {
      local_28 = param_3;
      FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_HOST\n");
      uVar1 = local_4c;
    }
    else if (local_4c == 0x102) {
      local_3c = param_3;
      FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_SETPLAYERORGROUPDATA\n");
      uVar1 = local_4c;
    }
    else {
      uVar1 = local_4c;
      if (local_4c == 0x103) {
        local_40 = param_3;
        FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_SETPLAYERORGROUPNAME\n");
        uVar1 = local_4c;
      }
    }
  }
  else {
    local_4c = local_4c - 0x105;
    uVar1 = local_4c;
    switch(local_4c) {
    case 0:
      local_c = param_3;
      FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_ADDGROUPTOGROUP\n");
      uVar1 = local_4c;
      break;
    case 1:
      local_1c = param_3;
      FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_DELETEGROUPFROMGROUP\n");
      uVar1 = local_4c;
      break;
    case 2:
      local_2c = param_3;
      FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_SECUREMESSAGE\n");
      uVar1 = local_4c;
      break;
    case 3:
      local_48 = param_3;
      FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_STARTSESSION\n");
      uVar1 = local_4c;
      break;
    case 4:
      local_14 = param_3;
      FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_CHAT\n");
      uVar1 = local_4c;
      break;
    case 5:
      local_38 = param_3;
      FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_SETGROUPOWNER\n");
      uVar1 = local_4c;
      break;
    case 8:
      local_30 = param_3;
      FUN__text__0042b2d0("DxPlay:SysMsg:DPSYS_SENDCOMPLETE\n");
      uVar1 = local_4c;
    }
  }
  local_4c = uVar1;
  local_8 = (uint *)0x41b43b;
  FUN__text__0056ce80();
  return;
}

