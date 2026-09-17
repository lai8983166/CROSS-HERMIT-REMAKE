
void FUN__text__0054cbb9(int param_1,int param_2,uint param_3)

{
  char cVar1;
  undefined4 uVar2;
  int iVar3;
  char *pcVar4;
  undefined4 local_c;
  ushort local_8;
  
  if ((*(uint *)(param_1 + 0x58) & 1) == 0) {
    FUN__text__0054381d(param_1,"Missing IHDR before tRNS");
  }
  else {
    if ((*(uint *)(param_1 + 0x58) & 4) != 0) {
      pcVar4 = "Invalid tRNS after IDAT";
LAB__text__0054cc2e:
      FUN__text__0054383b(param_1,pcVar4);
      FUN__text__0054c5c9(param_1,param_3);
      return;
    }
    if ((param_2 != 0) && ((*(byte *)(param_2 + 8) & 0x10) != 0)) {
      pcVar4 = "Duplicate tRNS chunk";
      goto LAB__text__0054cc2e;
    }
  }
  cVar1 = *(char *)(param_1 + 0x116);
  if (cVar1 == '\x03') {
    if ((*(byte *)(param_1 + 0x58) & 2) == 0) {
      FUN__text__0054383b(param_1,"Missing PLTE before tRNS");
LAB__text__0054cbff:
      if (param_3 != 0) {
        uVar2 = FUN__text__0054bc20(param_1,param_3);
        *(byte *)(param_1 + 0x5d) = *(byte *)(param_1 + 0x5d) | 0x20;
        *(undefined4 *)(param_1 + 0x15c) = uVar2;
        FUN__text__0054bcf9(param_1,uVar2,param_3);
        *(short *)(param_1 + 0x10a) = (short)param_3;
        goto LAB__text__0054cd25;
      }
      FUN__text__0054383b(param_1,"Zero length tRNS chunk");
    }
    else {
      if (param_3 <= *(ushort *)(param_1 + 0x108)) goto LAB__text__0054cbff;
      FUN__text__0054383b(param_1,"Incorrect tRNS chunk length");
    }
LAB__text__0054cd62:
    FUN__text__0054c5c9(param_1,param_3);
  }
  else {
    if (cVar1 == '\x02') {
      if (param_3 != 6) {
LAB__text__0054ccf0:
        pcVar4 = "Incorrect tRNS chunk length";
LAB__text__0054cd59:
        FUN__text__0054383b(param_1,pcVar4);
        goto LAB__text__0054cd62;
      }
      FUN__text__0054bcf9(param_1,&local_c,6);
      *(short *)(param_1 + 0x162) = (short)((local_c & 0xff) * 0x100 + (local_c >> 8 & 0xff));
      *(ushort *)(param_1 + 0x164) = (ushort)local_c._2_1_ * 0x100 + (ushort)local_c._3_1_;
      *(ushort *)(param_1 + 0x166) = local_8 * 0x100 + (local_8 >> 8);
    }
    else {
      if (cVar1 != '\0') {
        pcVar4 = "tRNS chunk not allowed with alpha channel";
        goto LAB__text__0054cd59;
      }
      if (param_3 != 2) goto LAB__text__0054ccf0;
      FUN__text__0054bcf9(param_1,&local_c,2);
      *(ushort *)(param_1 + 0x168) = (ushort)local_c * 0x100 + ((ushort)local_c >> 8);
    }
    *(undefined2 *)(param_1 + 0x10a) = 1;
LAB__text__0054cd25:
    iVar3 = FUN__text__0054c5c9(param_1,0);
    if (iVar3 == 0) {
      FUN__text__0054651e(param_1,param_2,*(undefined4 *)(param_1 + 0x15c),
                          *(undefined2 *)(param_1 + 0x10a),param_1 + 0x160);
    }
  }
  return;
}

