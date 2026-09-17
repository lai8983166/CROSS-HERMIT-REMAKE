
uint FUN__text__00584490(uint param_1,uint param_2)

{
  uint uVar1;
  
  uVar1 = FUN__text__00584560();
  uVar1 = param_1 & param_2 | uVar1 & ~param_2;
  FUN__text__005846e0(uVar1);
  return uVar1;
}

