
void FUN__text__00546772(undefined4 param_1,undefined4 *param_2)

{
  undefined4 *puVar1;
  int iVar2;
  undefined4 *puVar3;
  
  if ((param_2 != (undefined4 *)0x0) &&
     (puVar1 = (undefined4 *)*param_2, puVar1 != (undefined4 *)0x0)) {
    puVar3 = puVar1;
    for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar3 = 0;
      puVar3 = puVar3 + 1;
    }
    FUN__text__0054bc13(puVar1);
    *param_2 = 0;
  }
  return;
}

