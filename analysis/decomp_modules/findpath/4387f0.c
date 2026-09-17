
undefined4 FUN__text__004387f0(int param_1,int param_2)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [19];
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  cVar1 = ((char)*(undefined2 *)(param_2 + 2) - (char)*(undefined2 *)(param_1 + 2)) + '\x01';
  return CONCAT31(cVar1 >> 7,
                  (&DAT_005ff950)
                  [(int)cVar1 +
                   (char)(((char)*(undefined2 *)(param_2 + 4) - (char)*(undefined2 *)(param_1 + 4))
                         + '\x01') * 3]);
}

