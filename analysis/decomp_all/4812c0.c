
void __thiscall FUN__text__004812c0(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  char *local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (char *)(param_1 + 0x108f48);
  local_8 = param_1;
  FUN__text__00480fd0(param_2);
  if (((*local_c != '\0') && (iVar1 = FUN__text__0048e020(param_2,0xb), iVar1 == 0)) &&
     (iVar1 = FUN__text__0048e020(param_2,0xc), iVar1 == 0)) {
    FUN__text__00481360(param_2);
    FUN__text__0048f100(param_2);
  }
  local_8 = 0x48134b;
  FUN__text__0056ce80();
  return;
}

