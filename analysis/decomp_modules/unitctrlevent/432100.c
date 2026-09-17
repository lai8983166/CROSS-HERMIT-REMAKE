
void FUN__text__00432100(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  short *local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = &DAT_007f4488;
  iVar2 = FUN__text__00454c40();
  if ((iVar2 != 0) || (*(char *)(local_8 + 0x108b48) != '\0')) goto LAB__text__0043246e;
  local_10 = (int)*local_c;
  FUN__text__00430fe0(local_8 + 0x115cba);
  local_14 = local_10;
  if (local_10 < 0x97) {
    if (local_10 == 0x96) {
      FUN__text__00436a20();
      goto LAB__text__0043246e;
    }
    switch(local_10) {
    case 0:
      FUN__text__004326d0();
      break;
    case 1:
      FUN__text__00432b70();
      break;
    case 2:
      FUN__text__00433040();
      break;
    case 3:
      FUN__text__00433130();
      break;
    case 4:
      FUN__text__00433720();
      break;
    case 5:
      FUN__text__004337f0();
      break;
    case 6:
      FUN__text__00433970();
      break;
    case 7:
      FUN__text__00433a50();
      break;
    case 8:
      FUN__text__00433bd0();
      break;
    case 9:
      FUN__text__00433d00();
      break;
    case 10:
      FUN__text__00433f70();
      break;
    case 0xb:
      FUN__text__00434060();
      break;
    default:
      goto switchD__text__004321a1_caseD_c;
    case 0xd:
      FUN__text__00434300();
      break;
    case 0xe:
      FUN__text__004345b0();
      break;
    case 0xf:
      FUN__text__00434690();
      break;
    case 0x10:
      FUN__text__00434770();
      break;
    case 0x11:
      FUN__text__00434850();
      break;
    case 0x12:
      FUN__text__00434e90();
      break;
    case 0x14:
      FUN__text__00435080();
      break;
    case 0x15:
      FUN__text__00435190();
      break;
    case 0x16:
      FUN__text__004352f0();
      break;
    case 0x18:
      FUN__text__00435410();
      break;
    case 0x1d:
      FUN__text__004355a0();
      break;
    case 0x1f:
      FUN__text__004356b0();
      break;
    case 0x20:
      FUN__text__00435850();
      break;
    case 0x21:
      FUN__text__004359c0();
      break;
    case 0x23:
      FUN__text__00435aa0();
      break;
    case 0x25:
    case 0x26:
    case 0x27:
      FUN__text__00435b70();
      break;
    case 0x28:
      FUN__text__00435c30();
      break;
    case 0x29:
      FUN__text__00435cd0();
      break;
    case 0x2a:
      FUN__text__00435dc0();
      break;
    case 0x2b:
      FUN__text__00435f10();
      break;
    case 0x2c:
      FUN__text__004360b0();
      break;
    case 0x2d:
      FUN__text__004361a0();
      break;
    case 0x30:
    case 0x31:
    case 0x32:
    case 0x33:
    case 0x34:
    case 0x35:
    case 0x36:
    case 0x37:
    case 0x38:
    case 0x39:
    case 0x3a:
    case 0x3b:
    case 0x3c:
    case 0x3d:
    case 0x3e:
    case 0x3f:
    case 0x40:
    case 0x41:
    case 0x42:
    case 0x43:
      FUN__text__004362e0();
      break;
    case 0x44:
      FUN__text__00436460();
      break;
    case 0x47:
    case 0x48:
    case 100:
    case 0x65:
    case 0x66:
    case 0x67:
    case 0x68:
    case 0x69:
    case 0x6a:
    case 0x6b:
    case 0x6c:
    case 0x6d:
    case 0x6e:
    case 0x6f:
    case 0x70:
    case 0x71:
    case 0x72:
    case 0x73:
    case 0x74:
    case 0x75:
    case 0x76:
    case 0x77:
    case 0x78:
    case 0x79:
    case 0x7a:
    case 0x7b:
    case 0x7c:
    case 0x7d:
    case 0x7e:
    case 0x7f:
    case 0x80:
    case 0x81:
      FUN__text__004368b0();
      break;
    case 0x4c:
      FUN__text__00433a50();
      break;
    case 0x4d:
      FUN__text__00433d00();
      break;
    case 0x4e:
      FUN__text__00432b70();
      break;
    case 0x4f:
      FUN__text__00433040();
      break;
    case 0x50:
      FUN__text__00436500();
      break;
    case 0x52:
    case 0x53:
      FUN__text__004327e0();
      break;
    case 0x54:
    case 0x55:
    case 0x56:
    case 0x62:
      goto switchD__text__004321a1_caseD_54;
    }
  }
  else {
    local_14 = local_10 + -0x97;
    switch(local_10) {
    case 0x97:
      FUN__text__00436b40();
      break;
    case 0x98:
      FUN__text__00436c80();
      break;
    case 0x99:
      FUN__text__00436de0();
      break;
    case 0x9a:
      FUN__text__004370d0();
      break;
    default:
switchD__text__004321a1_caseD_c:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent.cpp",
                                  DAT_005ff750 + 0x9d,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 199:
      FUN__text__004373a0();
      break;
    case 0x180:
    case 0x181:
    case 0x182:
    case 0x186:
    case 0x18e:
    case 399:
switchD__text__004321a1_caseD_54:
    }
  }
LAB__text__0043246e:
  local_8 = 0x43247b;
  FUN__text__0056ce80();
  return;
}

