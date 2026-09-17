
void FUN__text__0054c84b(int param_1,int param_2,uint param_3)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  undefined1 *puVar6;
  char *pcVar7;
  int local_8;
  
  iVar2 = param_1;
  uVar1 = *(uint *)(param_1 + 0x58);
  if ((uVar1 & 1) == 0) {
    pcVar7 = "Missing IHDR before PLTE";
LAB__text__0054c877:
    FUN__text__0054381d(param_1,pcVar7);
LAB__text__0054c87f:
    *(uint *)(iVar2 + 0x58) = *(uint *)(iVar2 + 0x58) | 2;
    if (param_3 % 3 != 0) {
      pcVar7 = "Invalid palette chunk";
      if (*(char *)(iVar2 + 0x116) != '\x03') goto LAB__text__0054c89f;
      FUN__text__0054381d(iVar2,"Invalid palette chunk");
    }
    iVar4 = (int)param_3 / 3;
    iVar5 = FUN__text__00546672(iVar2,iVar4,3);
    *(byte *)(iVar2 + 0x5d) = *(byte *)(iVar2 + 0x5d) | 0x10;
    if (0 < iVar4) {
      puVar6 = (undefined1 *)(iVar5 + 2);
      local_8 = iVar4;
      do {
        FUN__text__0054bcf9(iVar2,&param_1,3);
        puVar6[-2] = (undefined1)param_1;
        puVar6[-1] = param_1._1_1_;
        *puVar6 = param_1._2_1_;
        puVar6 = puVar6 + 3;
        local_8 = local_8 + -1;
      } while (local_8 != 0);
    }
    FUN__text__0054c5c9(iVar2,0);
    iVar3 = param_2;
    *(int *)(iVar2 + 0x104) = iVar5;
    *(short *)(iVar2 + 0x108) = (short)iVar4;
    FUN__text__005464a6(iVar2,param_2,iVar5,iVar4);
    if ((((*(char *)(iVar2 + 0x116) == '\x03') && (iVar3 != 0)) &&
        ((*(byte *)(iVar3 + 8) & 0x10) != 0)) &&
       (*(ushort *)(iVar2 + 0x108) < *(ushort *)(iVar2 + 0x10a))) {
      FUN__text__0054383b(iVar2,"Truncating incorrect tRNS chunk length");
      *(ushort *)(iVar2 + 0x10a) = *(ushort *)(iVar2 + 0x108);
    }
  }
  else {
    if ((uVar1 & 4) == 0) {
      if ((uVar1 & 2) != 0) {
        pcVar7 = "Duplicate PLTE chunk";
        goto LAB__text__0054c877;
      }
      goto LAB__text__0054c87f;
    }
    pcVar7 = "Invalid PLTE after IDAT";
LAB__text__0054c89f:
    FUN__text__0054383b(iVar2,pcVar7);
    FUN__text__0054c5c9(iVar2,param_3);
  }
  return;
}

