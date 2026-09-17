
void __fastcall FUN__text__00428760(short *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  param_1[1] = param_1[3] + -1;
  param_1[2] = *param_1 - param_1[3];
  if (param_1[1] < 0) {
    param_1[1] = 0;
  }
  if (param_1[2] < 0) {
    param_1[2] = 0;
  }
  if (*param_1 <= param_1[1]) {
    param_1[1] = *param_1 + -1;
  }
  if (param_1[1] < 0) {
    param_1[1] = 0;
  }
  return;
}

