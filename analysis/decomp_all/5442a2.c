
void FUN__text__005442a2(int *param_1,int *param_2,int *param_3)

{
  int iVar1;
  undefined4 local_c;
  undefined4 local_8;
  
  iVar1 = 0;
  local_8 = 0;
  local_c = 0;
  if (param_1 != (int *)0x0) {
    local_8 = *param_1;
  }
  if (param_2 != (int *)0x0) {
    iVar1 = *param_2;
  }
  if (param_3 != (int *)0x0) {
    local_c = *param_3;
  }
  if (local_8 != 0) {
    FUN__text__00544170(local_8,iVar1,local_c);
  }
  if (iVar1 != 0) {
    FUN__text__0054bc13(iVar1);
    *param_2 = 0;
  }
  if (local_c != 0) {
    FUN__text__0054bc13(local_c);
    *param_3 = 0;
  }
  if (local_8 != 0) {
    FUN__text__0054bc13(local_8);
    *param_1 = 0;
  }
  return;
}

