
undefined4 FUN__text__004ab2e0(uint param_1)

{
  bool bVar1;
  undefined4 uVar2;
  int iVar3;
  ushort uVar4;
  undefined4 *puVar5;
  undefined4 local_54 [17];
  uint local_10;
  
  puVar5 = local_54;
  for (iVar3 = 0x14; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  bVar1 = true;
  uVar4 = 0;
  do {
    if ((int)DAT_007d57de <= (int)(uint)uVar4) {
LAB__text__004ab352:
      if (bVar1) {
        uVar2 = 0;
      }
      else {
        for (; local_10 = (uint)uVar4, (int)local_10 < (int)DAT_007d57de; uVar4 = uVar4 + 1) {
          *(undefined2 *)(&DAT_007d57e2 + local_10 * 2) =
               *(undefined2 *)(&DAT_007d57e4 + local_10 * 2);
        }
        DAT_007d57de = DAT_007d57de + -1;
        uVar2 = 1;
      }
      return uVar2;
    }
    if ((int)*(short *)(&DAT_007d57e2 + (uint)uVar4 * 2) == (param_1 & 0xffff)) {
      bVar1 = false;
      goto LAB__text__004ab352;
    }
    uVar4 = uVar4 + 1;
  } while( true );
}

