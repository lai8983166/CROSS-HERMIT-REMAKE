
char * __thiscall FUN__text__00466e20(int param_1,int param_2)

{
  char *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [17];
  int local_c;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  while( true ) {
    if (local_c == 0x200) {
      return (char *)0x0;
    }
    pcVar1 = (char *)(param_1 + 0x2a6f0 + local_c * 8);
    if ((*pcVar1 != '\0') && (*(short *)(pcVar1 + 2) == param_2)) break;
    local_c = local_c + 1;
  }
  return pcVar1;
}

