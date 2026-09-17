
char * __thiscall FUN__text__0041abf0(int param_1,int param_2)

{
  char *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = 0;
  while( true ) {
    if (local_10 == 0x10) {
      return (char *)0x0;
    }
    pcVar1 = (char *)(param_1 + 0x1780 + local_10 * 0x88);
    if ((*pcVar1 != '\0') && (*(int *)(pcVar1 + 0x84) == param_2)) break;
    local_10 = local_10 + 1;
  }
  return pcVar1;
}

