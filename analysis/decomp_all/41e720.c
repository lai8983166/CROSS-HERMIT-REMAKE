
void FUN__text__0041e720(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0041d790();
  if ((iVar1 == 0) || (*(char *)(local_8 + 0x22) == '\0')) {
    FUN__text__0041e6b0();
  }
  else {
    *(undefined4 *)(local_8 + 0x260) = param_1;
    *(int *)(local_8 + 0x264) = *(int *)(local_8 + 0x24c) + 5000;
    *(float *)(local_8 + 0x268) =
         (float)*(int *)(local_8 + 0x264) / (float)*(int *)(local_8 + 0x260);
    *(float *)(local_8 + 0x26c) = (float)*(int *)(local_8 + 0x24c);
    *(undefined4 *)(local_8 + 0x270) = 0;
    *(undefined4 *)(local_8 + 0x274) = 0;
  }
  local_8 = 0x41e7df;
  FUN__text__0056ce80();
  return;
}

