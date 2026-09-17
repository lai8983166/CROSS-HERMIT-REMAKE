
void FUN__text__004cd7b0(char *param_1,char *param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (; *param_2 = *param_1, *param_1 != '\0'; param_1 = param_1 + 1) {
    param_2 = param_2 + 1;
  }
  return;
}

