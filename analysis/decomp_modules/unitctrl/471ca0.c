
undefined4 __thiscall
FUN__text__00471ca0(int param_1,int param_2,int param_3,int param_4,int param_5,int *param_6,
                   int *param_7)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [17];
  int local_10;
  int local_c;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = param_3 + 0xf;
  do {
    if (local_10 == param_3 + 0xf + param_5) {
      return 0;
    }
    for (local_c = param_2 + 0xf; local_c != param_2 + 0xf + param_4; local_c = local_c + 1) {
      cVar1 = *(char *)(param_1 + 0x108f7c + local_10 * 0x1f + local_c);
      if (((cVar1 != -1) && (cVar1 != '\0')) && ((local_c != 0xf || (local_10 != 0xf)))) {
        *param_6 = local_c + -0xf;
        *param_7 = local_10 + -0xf;
        return 1;
      }
    }
    local_10 = local_10 + 1;
  } while( true );
}

