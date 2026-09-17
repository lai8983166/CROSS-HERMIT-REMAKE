
void FUN__text__0040b890(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [19];
  int local_10;
  int local_c;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (1 < DAT_00791730) {
    for (local_c = 0; local_10 = local_c, local_c != DAT_00791730 + -1; local_c = local_c + 1) {
      while (local_10 = local_10 + 1, local_10 != DAT_00791730) {
        if (*(int *)(*(int *)(&DAT_00791734 + local_10 * 4) + 0x18) <
            *(int *)(*(int *)(&DAT_00791734 + local_c * 4) + 0x18)) {
          uVar1 = *(undefined4 *)(&DAT_00791734 + local_10 * 4);
          *(undefined4 *)(&DAT_00791734 + local_10 * 4) =
               *(undefined4 *)(&DAT_00791734 + local_c * 4);
          *(undefined4 *)(&DAT_00791734 + local_c * 4) = uVar1;
        }
      }
    }
  }
  return;
}

