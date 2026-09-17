
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN__text__00540a0f(void)

{
  short sVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  bool bVar5;
  undefined4 uVar6;
  
  iVar4 = 0;
  _DAT_0080a388 = 0;
  DAT_0080a384 = 0;
  DAT_0080a37c = (short *)&DAT_00809f88;
  DAT_0080a378 = (undefined4 *)&DAT_008097b8;
  _DAT_00809f88 = 0;
LAB__text__00540a3f:
  DAT_0080a380 = -1;
LAB__text__00540a47:
  iVar2 = (int)(short)(&DAT_0075e6b8)[iVar4];
  if (iVar2 == 0) {
    if ((DAT_0080a380 < 0) && (DAT_0080a380 = FUN__text__0053fbc0(), DAT_0080a380 < 0)) {
      DAT_0080a380 = 0;
    }
    if (((((short)(&DAT_0075e7b0)[iVar4] != 0) &&
         (iVar2 = (short)(&DAT_0075e7b0)[iVar4] + DAT_0080a380, -1 < iVar2)) && (iVar2 < 0x108)) &&
       (*(short *)(&DAT_0075eb80 + iVar2 * 2) == DAT_0080a380)) {
      if (&UNK_0080a36d < DAT_0080a37c) goto LAB__text__00540dea;
      iVar4 = (int)*(short *)(&DAT_0075e970 + iVar2 * 2);
      DAT_0080a37c = DAT_0080a37c + 1;
      *DAT_0080a37c = *(short *)(&DAT_0075e970 + iVar2 * 2);
      DAT_0080a378 = DAT_0080a378 + 1;
      *DAT_0080a378 = DAT_0080a370;
      DAT_0080a380 = -1;
      if (0 < DAT_0080a384) {
        DAT_0080a384 = DAT_0080a384 + -1;
      }
      goto LAB__text__00540a47;
    }
    if ((((short)(&DAT_0075e878)[iVar4] != 0) &&
        (iVar2 = (short)(&DAT_0075e878)[iVar4] + DAT_0080a380, -1 < iVar2)) &&
       ((iVar2 < 0x108 && (*(short *)(&DAT_0075eb80 + iVar2 * 2) == DAT_0080a380)))) {
      iVar2 = (int)*(short *)(&DAT_0075e970 + iVar2 * 2);
      goto LAB__text__00540b2d;
    }
    if (DAT_0080a384 == 0) {
      FUN__text__0053eb92(DAT_0080a390,"syntax error");
      _DAT_0080a388 = _DAT_0080a388 + 1;
    }
    if (2 < DAT_0080a384) goto LAB__text__00540de1;
    DAT_0080a384 = 3;
    while ((((short)(&DAT_0075e7b0)[*DAT_0080a37c] == 0 ||
            (iVar4 = (short)(&DAT_0075e7b0)[*DAT_0080a37c] + 0x100, iVar4 < 0)) ||
           ((0x107 < iVar4 || (*(short *)(&DAT_0075eb80 + iVar4 * 2) != 0x100))))) {
      if (DAT_0080a37c < &UNK_00809f89) {
        DAT_0080a384 = 3;
        return 1;
      }
      DAT_0080a37c = DAT_0080a37c + -1;
      DAT_0080a378 = DAT_0080a378 + -1;
    }
    if (&UNK_0080a36d < DAT_0080a37c) goto LAB__text__00540dea;
    sVar1 = *(short *)(&DAT_0075e970 + iVar4 * 2);
    DAT_0080a37c = DAT_0080a37c + 1;
    *DAT_0080a37c = sVar1;
    uVar6 = DAT_0080a370;
  }
  else {
LAB__text__00540b2d:
    iVar4 = (int)*(short *)(&DAT_0075e650 + iVar2 * 2);
    DAT_0080a374 = DAT_0080a378[1 - iVar4];
    switch(iVar2) {
    case 1:
      uVar6 = 0;
      break;
    case 2:
      uVar6 = 1;
      break;
    case 3:
      uVar6 = 4;
      break;
    case 4:
      uVar6 = 5;
      break;
    case 5:
      uVar6 = 6;
      break;
    case 6:
      uVar6 = 7;
      break;
    case 7:
      uVar6 = 8;
      break;
    case 8:
      uVar6 = 9;
      break;
    case 9:
      uVar6 = 10;
      break;
    case 10:
      uVar6 = 0xb;
      break;
    case 0xb:
      uVar6 = 0xc;
      break;
    case 0xc:
      uVar6 = 0xd;
      break;
    case 0xd:
      uVar6 = 0xe;
      break;
    case 0xe:
      uVar6 = 0xf;
      break;
    case 0xf:
      uVar6 = 0x10;
      break;
    case 0x10:
      uVar6 = 0x11;
      break;
    case 0x11:
      uVar6 = 0x12;
      break;
    case 0x12:
      uVar6 = 0x13;
      break;
    case 0x13:
      uVar6 = 0x14;
      break;
    case 0x14:
      uVar6 = 0x15;
      break;
    case 0x15:
      uVar6 = 0x16;
      break;
    case 0x16:
      uVar6 = 0x17;
      break;
    case 0x17:
      uVar6 = 0x18;
      break;
    case 0x18:
      uVar6 = 0x19;
      break;
    case 0x19:
      uVar6 = 0x1a;
      break;
    case 0x1a:
      uVar6 = 0x1b;
      break;
    case 0x1b:
      uVar6 = 0x1c;
      break;
    case 0x1c:
      uVar6 = 0x1d;
      break;
    case 0x1d:
      uVar6 = 0x1e;
      break;
    case 0x1e:
      uVar6 = 0x1f;
      break;
    case 0x1f:
      uVar6 = 0x20;
      break;
    case 0x20:
      uVar6 = 0x21;
      break;
    case 0x21:
      uVar6 = 0x22;
      break;
    case 0x22:
      uVar6 = 0x23;
      break;
    case 0x23:
      uVar6 = 0x24;
      break;
    case 0x24:
      uVar6 = 0x25;
      break;
    case 0x25:
      uVar6 = 0x26;
      break;
    case 0x26:
      uVar6 = 0x27;
      break;
    case 0x27:
      uVar6 = 0x28;
      break;
    case 0x28:
      uVar6 = 0x29;
      break;
    case 0x29:
      uVar6 = 0x2a;
      break;
    case 0x2a:
      uVar6 = 0x2b;
      break;
    case 0x2b:
      uVar6 = 0x2c;
      break;
    case 0x2c:
      uVar6 = 0x2d;
      break;
    case 0x2d:
      uVar6 = 0x2e;
      break;
    case 0x2e:
      uVar6 = 0x2f;
      break;
    case 0x2f:
      uVar6 = 0x30;
      break;
    case 0x30:
      uVar6 = 0x31;
      break;
    case 0x31:
      uVar6 = 0x32;
      break;
    default:
      goto switchD__text__00540b57_default;
    }
    FUN__text__005400d8(uVar6);
switchD__text__00540b57_default:
    DAT_0080a37c = DAT_0080a37c + -iVar4;
    iVar3 = (int)*DAT_0080a37c;
    DAT_0080a378 = DAT_0080a378 + -iVar4;
    if ((iVar3 == 0) && (*(short *)(&DAT_0075e5e8 + iVar2 * 2) == 0)) {
      DAT_0080a37c = DAT_0080a37c + 1;
      iVar4 = 3;
      *DAT_0080a37c = 3;
      DAT_0080a378 = DAT_0080a378 + 1;
      *DAT_0080a378 = DAT_0080a374;
      bVar5 = DAT_0080a380 == 0;
      if (DAT_0080a380 < 0) {
        DAT_0080a380 = FUN__text__0053fbc0();
        bVar5 = DAT_0080a380 == 0;
        if (DAT_0080a380 < 0) {
          DAT_0080a380 = 0;
          bVar5 = true;
        }
      }
      if (bVar5) {
        return 0;
      }
      goto LAB__text__00540a47;
    }
    iVar4 = *(short *)(&DAT_0075e5e8 + iVar2 * 2) * 2;
    if ((((*(short *)(&DAT_0075e940 + iVar4) == 0) ||
         (iVar2 = *(short *)(&DAT_0075e940 + iVar4) + iVar3, iVar2 < 0)) || (0x107 < iVar2)) ||
       (*(short *)(&DAT_0075eb80 + iVar2 * 2) != iVar3)) {
      sVar1 = *(short *)(&DAT_0075e780 + iVar4);
    }
    else {
      sVar1 = *(short *)(&DAT_0075e970 + iVar2 * 2);
    }
    if (&UNK_0080a36d < DAT_0080a37c) {
LAB__text__00540dea:
      FUN__text__0053eb92(DAT_0080a390,"yacc stack overflow");
      return 1;
    }
    DAT_0080a37c = DAT_0080a37c + 1;
    *DAT_0080a37c = sVar1;
    uVar6 = DAT_0080a374;
  }
  iVar4 = (int)sVar1;
  DAT_0080a378 = DAT_0080a378 + 1;
  *DAT_0080a378 = uVar6;
  goto LAB__text__00540a47;
LAB__text__00540de1:
  if (DAT_0080a380 == 0) {
    return 1;
  }
  goto LAB__text__00540a3f;
}

