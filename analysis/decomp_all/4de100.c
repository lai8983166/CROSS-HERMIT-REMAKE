
void FUN__text__004de100(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  undefined *local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                              DAT_00738ca0 + 8,0);
  if (iVar2 != 0) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((param_2 == -1) &&
     (iVar2 = FUN__text__00424f80("skill != -1","E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                  DAT_00738ca0 + 0xb,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((100 < param_2) &&
     (iVar2 = FUN__text__00424f80("skill <= (100)","E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp"
                                  ,DAT_00738ca0 + 0xc,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_10 = &DAT_006c2dc8 + param_2 * 0x48;
  local_c = &DAT_006b2d88 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40;
  local_14 = *(undefined4 *)(param_1 + 600);
  local_18 = param_2 + -1;
  switch(param_2) {
  case 1:
  case 3:
  case 5:
  case 8:
  case 9:
  case 10:
  case 0xc:
  case 0xd:
  case 0x10:
  case 0x11:
  case 0x12:
  case 0x14:
  case 0x19:
  case 0x1b:
  case 0x1e:
  case 0x21:
  case 0x32:
  case 0x42:
    break;
  case 2:
    break;
  case 4:
  case 6:
  case 7:
  case 0x22:
  case 0x29:
  case 0x2c:
  case 0x2d:
  case 0x2e:
  case 0x30:
  case 0x31:
  case 0x35:
  case 0x37:
  case 0x4d:
  case 0x4e:
  case 0x50:
  case 0x52:
  case 0x53:
  case 0x54:
    break;
  case 0xb:
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_005ca4fc,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                DAT_00738ca0 + 0xe0,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    break;
  case 0xf:
    break;
  case 0x1d:
    break;
  case 0x1f:
    break;
  case 0x20:
    break;
  case 0x23:
    break;
  case 0x24:
    break;
  case 0x25:
    break;
  case 0x26:
    break;
  case 0x28:
    break;
  case 0x2a:
    break;
  case 0x2b:
    break;
  case 0x2f:
    break;
  case 0x34:
    break;
  case 0x36:
    break;
  case 0x39:
    break;
  case 0x3a:
    break;
  case 0x3b:
    break;
  case 0x3c:
    break;
  case 0x40:
    break;
  case 0x41:
    break;
  case 0x43:
    break;
  case 0x45:
    break;
  case 0x46:
    break;
  case 0x47:
    break;
  case 0x48:
    break;
  case 0x49:
    break;
  case 0x4a:
    break;
  case 0x4b:
    break;
  case 0x4c:
    break;
  case 0x51:
  }
  local_8 = 0x4de809;
  FUN__text__0056ce80();
  return;
}

