
void __thiscall FUN__text__0044aee0(int param_1,int param_2)

{
  char *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [18];
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  pcVar1 = (char *)(param_1 + 0x1ab0 + param_2 * 8);
  if (*pcVar1 != '\0') {
    pcVar1[1] = pcVar1[1] ^ 1;
  }
  return;
}

