
int * __fastcall FUN__text__005525b6(int param_1)

{
  byte *pbVar1;
  int in_EAX;
  int *piVar2;
  int iVar3;
  undefined1 *puVar4;
  int *piVar5;
  
  piVar2 = (int *)(*(code *)**(undefined4 **)(in_EAX + 4))();
  puVar4 = &DAT_005d41b0;
  piVar5 = piVar2;
  do {
    iVar3 = 0;
    do {
      pbVar1 = puVar4 + iVar3;
      iVar3 = iVar3 + 1;
      *piVar5 = (int)((uint)*pbVar1 * -0x1fe + 0xfe01) / (param_1 * 0x200 + -0x200);
      piVar5 = piVar5 + 1;
    } while (iVar3 < 0x10);
    puVar4 = puVar4 + 0x10;
  } while ((int)puVar4 < 0x5d42b0);
  return piVar2;
}

