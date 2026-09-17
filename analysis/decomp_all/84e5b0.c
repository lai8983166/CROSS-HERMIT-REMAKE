
undefined4 FUN__text1__0084e5b0(byte *param_1,char *param_2,int param_3)

{
  char cVar1;
  byte bVar2;
  ushort uVar3;
  uint uVar4;
  undefined4 uVar5;
  uint uVar6;
  bool bVar7;
  
  uVar5 = 0;
  if (param_3 != 0) {
    if (DAT_008758bc == 0) {
      do {
        bVar2 = *param_1;
        cVar1 = *param_2;
        uVar3 = CONCAT11(bVar2,cVar1);
        if (bVar2 == 0) break;
        uVar3 = CONCAT11(bVar2,cVar1);
        uVar6 = (uint)uVar3;
        if (cVar1 == '\0') break;
        param_1 = param_1 + 1;
        param_2 = param_2 + 1;
        if ((0x40 < bVar2) && (bVar2 < 0x5b)) {
          uVar6 = (uint)CONCAT11(bVar2 + 0x20,cVar1);
        }
        uVar3 = (ushort)uVar6;
        bVar2 = (byte)uVar6;
        if ((0x40 < bVar2) && (bVar2 < 0x5b)) {
          uVar3 = (ushort)CONCAT31((int3)(uVar6 >> 8),bVar2 + 0x20);
        }
        bVar2 = (byte)(uVar3 >> 8);
        bVar7 = bVar2 < (byte)uVar3;
        if (bVar2 != (byte)uVar3) goto LAB__text1__0084e60b;
        param_3 = param_3 + -1;
      } while (param_3 != 0);
      uVar5 = 0;
      bVar2 = (byte)(uVar3 >> 8);
      bVar7 = bVar2 < (byte)uVar3;
      if (bVar2 != (byte)uVar3) {
LAB__text1__0084e60b:
        uVar5 = 0xffffffff;
        if (!bVar7) {
          uVar5 = 1;
        }
      }
    }
    else {
      uVar4 = 0;
      uVar6 = 0;
      do {
        uVar4 = CONCAT31((int3)(uVar4 >> 8),*param_1);
        uVar6 = CONCAT31((int3)(uVar6 >> 8),*param_2);
        if ((uVar4 == 0) || (uVar6 == 0)) break;
        param_1 = param_1 + 1;
        param_2 = param_2 + 1;
        uVar6 = FUN__text1__0084e65d(uVar6,uVar4);
        uVar4 = FUN__text1__0084e65d();
        bVar7 = uVar4 < uVar6;
        if (uVar4 != uVar6) goto LAB__text1__0084e64d;
        param_3 = param_3 + -1;
      } while (param_3 != 0);
      uVar5 = 0;
      bVar7 = uVar4 < uVar6;
      if (uVar4 != uVar6) {
LAB__text1__0084e64d:
        uVar5 = 0xffffffff;
        if (!bVar7) {
          uVar5 = 1;
        }
      }
    }
  }
  return uVar5;
}

