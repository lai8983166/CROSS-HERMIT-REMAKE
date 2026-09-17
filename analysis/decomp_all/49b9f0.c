
void __fastcall FUN__text__0049b9f0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1 + 0x108b3e;
  local_8 = param_1;
  FUN__text__0043d270((int)*(short *)(param_1 + 0x108b40),(int)*(short *)(param_1 + 0x108b42),
                      (int)*(char *)(param_1 + 0x108b4b));
  local_8 = 0x49ba4d;
  FUN__text__0056ce80();
  return;
}

