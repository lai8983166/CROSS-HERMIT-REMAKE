
uint __fastcall FUN__text__00446e90(int param_1)

{
  char cVar1;
  byte bVar2;
  int iVar3;
  char cVar4;
  undefined4 *puVar5;
  undefined4 local_4c [18];
  
  puVar5 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  cVar4 = *(char *)(param_1 + 0x1bd3) * 'd' + *(char *)(param_1 + 0x1bd4) * '\n' +
          *(char *)(param_1 + 0x1bd5);
  cVar1 = *(char *)(param_1 + 0x1bd6) * 'd' + *(char *)(param_1 + 0x1bd7) * '\n' +
          *(char *)(param_1 + 0x1bd8);
  bVar2 = *(char *)(param_1 + 0x1bd9) * 'd' + *(char *)(param_1 + 0x1bda) * '\n' +
          *(char *)(param_1 + 0x1bdb);
  return CONCAT13(bVar2,CONCAT12(cVar1,CONCAT11(cVar4,*(char *)(param_1 + 0x1bd0) * 'd' +
                                                      *(char *)(param_1 + 0x1bd1) * '\n' +
                                                      *(char *)(param_1 + 0x1bd2)))) << 0x18 |
         (CONCAT12(bVar2,CONCAT11(cVar1,cVar4)) & 0xff) << 0x10 |
         (CONCAT11(bVar2,cVar1) & 0xff) << 8 | (uint)bVar2;
}

