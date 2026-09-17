
int FUN__text__004d5590(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [17];
  int local_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_c = 2; (local_c < 0x33 && (*(int *)(&UNK_006252fc + local_c * 4) <= param_1));
      local_c = local_c + 1) {
  }
  return local_c + -1;
}

