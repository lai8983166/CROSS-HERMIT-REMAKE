
void __thiscall FUN__text__00428480(short *param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  short *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 == 0) {
    param_2 = 0;
  }
  if (param_2 < 0) {
    param_2 = 0;
  }
  if (*param_1 <= param_2) {
    param_2 = *param_1 + -1;
  }
  local_8 = param_1;
  FUN__text__00428760();
  while (local_c = FUN__text__00428310(), local_c != param_2) {
    FUN__text__00428520();
  }
  local_8 = (short *)0x42850f;
  FUN__text__0056ce80();
  return;
}

